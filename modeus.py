import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json
import ast

month = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря',
}

load_dotenv()
cookies_env = os.getenv('MODEUS_COOKIE')
cookies = ast.literal_eval(cookies_env)
headers_env = os.getenv("MODEUS_HEADERS")
headers = ast.literal_eval(headers_env)

json_data_for_id_search = {
    'sort': '+fullName',
    'size': 10,
    'page': 0,
}

week_day = datetime.now().weekday()
time_delta = timedelta(days=week_day)
date_min = datetime.now().date() - time_delta
time_delta = timedelta(days=6-week_day)
date_max = datetime.now().date() + time_delta

json_data_for_lession_parsing = {
    'size': 500,
    'timeMin': f'{date_min}T00:00:00+05:00',
    'timeMax': f'{date_max}T23:59:59+05:00',
    'attendeePersonId': [
        '05f08994-60bb-431f-9a8a-e3fd4b35ae0b',
    ],
}

def get_json_id(fio):
    json_data_for_id_search['fullName'] = fio
    response = requests.post('https://utmn.modeus.org/schedule-calendar-v2/api/people/persons/search', cookies=cookies, headers=headers, json=json_data_for_id_search).json()
    json_id = response['_embedded']['persons'][0]['id']
    return str(json_id)

def get_rasps(fio):
    json_data_for_lession_parsing['attendeePersonId'] = [get_json_id(fio)]
    response = requests.post('https://utmn.modeus.org/schedule-calendar-v2/api/calendar/events/search?tz=Asia/Tyumen&authAction=', cookies=cookies, headers=headers, json=json_data_for_lession_parsing).json()

    paras = []
    # проход по всем парам
    for lession in response['_embedded']['events']:
        event_id = lession['id'] # айди ивента зантия
        name = lession['name'] # тема пары
        course_name_id = lession['_links']['course-unit-realization']['href'].split('/')[1]

        # поиск названия предмета
        for course in response['_embedded']['course-unit-realizations']:
            if course_name_id == course['id']:
                course_name = course['name']
                course_name_short = course['nameShort']

        # время начала и конца пар
        start_time = lession['startsAtLocal'].split('T')[1]
        end_time = lession['endsAtLocal'].split('T')[1]
        date = (lession['startsAtLocal'].split('T')[0].split('-')[2] + '.' + lession['startsAtLocal'].split('T')[0].split('-')[1] + '.' + lession['startsAtLocal'].split('T')[0].split('-')[0])

        # поиск аудитории
        for event_location in response['_embedded']['event-locations']:
            if event_id == event_location['eventId']:
                try:
                    event_locations_href = event_location['_links']['event-rooms']['href'].split('/')[1]
                except KeyError:
                    room = event_location['customLocation']
                    break
                for event_room in response['_embedded']['event-rooms']:
                    if event_locations_href == event_room['id']:
                        event_rooms_href = event_room['_links']['room']['href'].split('/')[1]
                        for rooms in response['_embedded']['rooms']:
                            if event_rooms_href == rooms['id']:
                                room = rooms['name']

        paras.append([(course_name_short + ' / ' + course_name), room, date, str(start_time), str(end_time)])

    weekly_days_sorted = []
    for i in paras:
        weekly_days_sorted = set(weekly_days_sorted)
        weekly_days_sorted.add(i[2].split('.')[0])
        weekly_days_sorted = list(weekly_days_sorted)
    weekly_days_sorted.sort()

    times_sorted = []
    for i in paras:
        times_sorted = set(times_sorted)
        times_sorted.add(i[3].split(':')[0])
        times_sorted = list(times_sorted)
    times_sorted.sort()

    paras_sorted_by_days_and_time = []
    for week_day in weekly_days_sorted:
        for time_day in times_sorted:
            for j in paras:
                if week_day == j[2].split('.')[0] and time_day == j[3].split(':')[0]:
                    paras_sorted_by_days_and_time.append(j)

    weekly_days_sorted_clone = []

    json_data_for_lession_parsing['attendeePersonId'] = get_json_id(fio)
    res = ''
    current_month = month[datetime.now().month]
    for i in weekly_days_sorted:
        weekly_days_sorted_clone.append(i)
    for para in paras_sorted_by_days_and_time:
        if para[2].split('.')[0] in weekly_days_sorted_clone:
            res += ('\n' + '-------------------------------------------\n\n' + (para[2].split('.')[0] + ' ' + current_month + ':')) + '\n\n'
            weekly_days_sorted_clone.remove(para[2].split('.')[0])
        res += (para[0] + ' ' + para[2] + ' ' + (para[3] + ' — ' + para[4]) + ' ' + para[1]) + '\n' 
    res += '\n-------------------------------------------'
    return res

if __name__ == '__main__':
    print(get_rasps(input('Введи своё ФИО: ')))