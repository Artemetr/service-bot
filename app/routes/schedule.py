import json

from flask import request

from app import app

schedule_mock = {
    'ТИУ': {
        'АСОиУб 18 1': {
            'нечетная': {
                'понедельник': [
                    {
                        'все': {
                            'время начала': '10:30',
                            'время окончания': '10:30',
                            'название': 'Название предмета',
                            'преподаватель': 'Лаптева У. В.'
                        }
                    }
                ]
            },
            'четная': {

            }
        }
    }
}


@app.route('/schedule', methods=['POST'])
def schedule():
    response = {
        'version': request.json['version'],
        'session': request.json['session'],
        'response': {
            'end_session': False,
            'text': 'Some text',
            'buttons': [
                {
                    "title": "Ладно",
                    "url": "https://market.yandex.ru/search?text=слон",
                    "hide": True
                }
            ]
        }
    }

    if request.json['request']['original_utterance'].lower() in [
        'какое расписание',
        'расписание'
    ]:
        response['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )
