import json
import re
import sys

import requests
from bs4 import BeautifulSoup


def parse_class(content, start_time, end_time):
    re_search = re.search(r'([\w\s]+)\s(\w+\s\w.\w.)\((\w+)\),\s(\d+)\(\w+\s(\d+)\)', content)

    return {
        'startTime': start_time,
        'endTime': end_time,
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
    result = {day: [] for day in days}
    for tr in tbody.findChildren('tr', recursive=False):
        tds = tr.findChildren('td', recursive=False)
        [start_time, end_time] = tds[1].text.split(' - ')
        for td, day in zip(tds[2:], days):
            if not td.table:
                continue
            sub_tds = td.table.findChildren('td', recursive=False)
            items = [parse_class(sub_td.text, start_time, end_time) for sub_td in sub_tds]
            if len(items) == 1:
                items_type = 'forAll'
                items = items[0]
            else:
                items_type = 'subgroups'

            result[day].append({items_type: items})

    return result


def parse(url):
    soup = BeautifulSoup(
        requests.get(url).content.decode('koi8-r'), 'lxml')

    tbodies = soup.select('tbody')
    return {
        'odd': parse_week(tbodies[0]),
        'even': parse_week(tbodies[1])
    }


if __name__ == '__main__':
    print(json.dumps(parse(sys.argv[1])))
