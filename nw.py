#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'yorick'

import time
import sys
from browser import NW

sys.path.append('..')
try:
    from settings import *
except:
    raise Exception("Settings.py not found!")

TIME_CYCLE_SLEEP = 60
BASE_URL = "https://gateway.nw.ru.perfectworld.eu/"
PROFS = (u'Обработка кожи',
         u'Лидерство',
         u'Изготовление оружия',
         u'Алхимия',
         u'Изготовление лат',
         u'Кройка и шитье',
         u'Ювелирное дело',
         u'Обработка черного льда',
         u'Нанесение узоров',
         u'Плетение кольчуг',
)

sleep_time = 5
nw = NW(BASE_URL, cookies)
time.sleep(2)
nw.login(useremail, password)
time.sleep(sleep_time)
nw.select_character(character_name)
time.sleep(sleep_time)
nw.select_menu_item(u'Профессии')
time.sleep(sleep_time)

while True:
    tasks_finished = nw.get_finished_tasks()
    if len(tasks_finished):
        # выполняем task_callback у 1го таска
        tasks_finished[0]()
    for task_callback in tasks_finished:
        # task_callback()
        time.sleep(5)
        nw.finish_task()
    free_slots = nw.get_free_slots()
    for i in xrange(len(free_slots)):
        if i > 0:
            free_slots = nw.get_free_slots()
        # выполняем callback у 1го слота
        free_slots[0]()
        time.sleep(5)
        nw.profession_click(u'Обработка кожи')
        time.sleep(5)
        nw.run_new_task(u'Соберите экзотические шкуры')
    time.sleep(TIME_CYCLE_SLEEP)

