import json
import re
import datetime

from flask import request

from app import app
from lib.schedule import models


def ref_date(date: datetime.datetime, time):
    [hour, minute] = re.findall(r'(\d+):(\d+)', time)[0]
    return datetime.datetime(date.year, date.month, date.day, int(hour), int(minute))


def with_subgroup(lesson, subgroup=1):
    return lesson.get('subgroups')[subgroup - 1] if lesson.get('subgroups') else lesson.get('forAll') or {}


def voice_message(lesson, subgroup=1):
    lesson_data = with_subgroup(lesson, subgroup)
    result = f'В {lesson.get("startTime")} будет '
    if lesson_data:
        result += f'{lesson_data.get("name")} у {lesson_data.get("teacher")} {lesson_data.get("location")}'
    else:
        result += 'свободное время'

    return result + '.'


def voice_processing(lessons, subgroup=1):
    return '\n'.join([voice_message(lesson, subgroup) for number, lesson in zip(list(range(len(lessons))), lessons)])


@app.route('/schedule', methods=['POST'])
def schedule_handler():
    response = {
        'version': request.json['version'],
        'session': request.json['session'],
        'response': {
            'end_session': False,
            'text': 'Some text',
            # 'buttons': [
            #     {
            #         "title": "Ладно",
            #         "url": "https://market.yandex.ru/search?text=слон",
            #         "hide": True
            #     }
            # ]
        }
    }

    print(request.json)
    user_phrase = request.json['request']['original_utterance'].lower()
    if not user_phrase:
        return json.dumps(
            response,
            ensure_ascii=False,
            indent=2
        )

    if re.findall('следующий день', user_phrase):
        today_diff = 1
    else:
        when = {
            'понедельник': 1 - datetime.datetime.today().isocalendar()[2],
            'вторник': 2 - datetime.datetime.today().isocalendar()[2],
            'сред': 3 - datetime.datetime.today().isocalendar()[2],
            'четверг': 4 - datetime.datetime.today().isocalendar()[2],
            'пятниц': 5 - datetime.datetime.today().isocalendar()[2],
            'суббот': 6 - datetime.datetime.today().isocalendar()[2],
            'воскресен': 7 - datetime.datetime.today().isocalendar()[2],
            'завтра': 1,
            'послезавтра': 2,
            'вчера': -1,
            'позавчера': -2,
            'сегодня': 0,
        }

        today_diffs = [value + 7 if re.findall(f'ий {key}', user_phrase) else value for key, value in when.items() if
                       re.findall(key, user_phrase)]
        today_diff = today_diffs[0] if len(today_diffs) else 0

    needed_date = datetime.datetime.now() + datetime.timedelta(days=today_diff)
    week = 'odd' if needed_date.isocalendar()[1] % 2 else 'even'

    group: models.EducationalGroup = models.EducationalGroup.get_with_id(1)
    week_schedule = group.schedule.get(week) if group.schedule.get(week) else group.schedule.get('invariably')
    day_schedule = week_schedule[needed_date.isocalendar()[2] - 1]
    time_ranges = {number + 1: {'startTime': ref_date(needed_date, lesson.get('startTime')),
                                'endTime': ref_date(needed_date, lesson.get('endTime'))} for number, lesson in
                   zip(range(len(day_schedule)), day_schedule)}

    if re.findall(r'следующ(ий|ая|ее) (пара|урок|лекция|практика|занятие)', user_phrase):
        number = int(min([key for key, value in time_ranges.items() if value.get('startTime') > needed_date] or [0]))
        number = number + 1 if number else number
    elif re.findall(r'пара|урок|лекция|практика|занятие', user_phrase):
        number = int(min([key for key, value in time_ranges.items() if value.get('startTime') > needed_date] or [0]))
    else:
        numbers = {
            'перв': 1,
            'втор': 2,
            'трет': 3,
            'четвё': 4,
            'пятая|пятый': 5,
            'шест': 6,
            'сед': 7,
            'восьм': 8,
            'дев': 9,
            'дес': 10,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10
        }
        number = int(min([value for key, value in numbers.items() if re.findall(key, user_phrase)] or [0]))

    if number:
        lessons = [day_schedule[number]]
    else:
        lessons = day_schedule

    response['response']['text'] = voice_processing(lessons, 1)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )
