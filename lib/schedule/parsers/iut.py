import re

import requests
from bs4 import BeautifulSoup

from lib.schedule.db import Session
from lib.schedule.models.educational_group import EducationalGroup


def parse_class(content):
    re_search = re.search(r'([\w\s]+)\s(\w+\s\w.\w.)\((\w+)\),\s(\d+)\(\w+\s(\d+)\)', content)

    return {
        'teacher': re_search.group(2),
        'location': f'{re_search.group(4)} аудитория {re_search.group(5)} корпус',
        'name': re_search.group(1),
        'type': {
            'лаб': 'лабораторная работа',
            'пр': 'практика',
            'л': 'лекция'
        }[re_search.group(3)]
    } if re_search else {}


def parse_week(tbody):
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    days = list(range(7))
    result = [[] for day in days]
    for tr in tbody.findChildren('tr', recursive=False):
        tds = tr.findChildren('td', recursive=False)
        [start_time, end_time] = tds[1].text.split(' - ')
        for td, day in zip(tds[2:], days):
            append_item = {
                "startTime": start_time,
                "endTime": end_time
            }
            if td.table:
                sub_tds = td.table.findChildren('td', recursive=False)
                items = [parse_class(sub_td.text) for sub_td in sub_tds]
                if len(items) == 1:
                    items_type = 'forAll'
                    items = items[0]
                else:
                    items_type = 'subgroups'
                append_item[items_type] = items

            result[day].append(append_item)

    return result


def parse(url):
    soup = BeautifulSoup(
        requests.get(url).content.decode('koi8-r'), 'lxml')

    tbodies = soup.select('tbody')
    return {
        'odd': parse_week(tbodies[0]),
        'even': parse_week(tbodies[1])
    }


def parse_for_group(group: EducationalGroup):
    group.schedule = parse(group.url)


def parse_for_group_id(group_id: int):
    with Session() as s:
        group: EducationalGroup = s.query(EducationalGroup).filter(EducationalGroup.id == group_id).one_or_none()
        parse_for_group(group)
        s.commit()
