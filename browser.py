#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'yorick'

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from log import log

logger = log()


class NW():
    def __init__(self, base_url, cookies):
        self.driver = webdriver.Firefox()
        self.driver.get('https://gateway.nw.ru.perfectworld.eu/faq.html')
        self.base_url = base_url
        logger.log("page loaded")
        for cookie_name in cookies:
            print "set cookie: %s -> %s" % (cookie_name, cookies[cookie_name])
            self.driver.add_cookie({'name': cookie_name, 'value': cookies[cookie_name], 'path': '/'})
        self.driver.get(base_url)
        # print driver.title
        assert 'Neverwinter' in self.driver.title
        for cookie in self.driver.get_cookies():
            print "read cookies: %s -> %s" % (cookie['name'], cookie['value'])


    def login(self, useremail, passwd):
        elem = self.driver.find_element_by_id('user')
        elem.send_keys(useremail)

        elem = self.driver.find_element_by_id('pass')
        elem.send_keys(passwd + Keys.RETURN)
        logger.log(u"Зашел")

    def select_character(self, char_name):
        logger.log("page: " + self.driver.title)
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "charselect"))
            )
        except:
            logger.log("element with class 'charselect' not found")
            return False
        # elem = self.driver.find_element_by_class_name('charselect')
        # print elem, type(elem), elem.text
        links = elem.find_elements_by_tag_name('a')
        assert links
        for link in links:
            if char_name in link.text:
                # print link, type(link), link.text
                link.click()

    def select_menu_item(self, sheet):
        '''
        sheets = (u'Листок персонажа', u'Инвентарь', u'Профессии', u'Аукционный дом', u'Биржа астральных бриллиантов', u'Рынок ZEN', u'Гильдия', u'Почта')
        '''
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.title_is(u'Портал Neverwinter')
            )
        except:
            logger.log(u"неожиданный заголовок html - " + self.driver.title)
            return False

        logger.log("page: " + self.driver.title)
        # assert u'Портал Neverwinter' in self.driver.title
        elem = self.driver.find_element_by_class_name('button-list')
        # print elem, type(elem), elem.text
        links = elem.find_elements_by_tag_name('a')
        assert links
        for link in links:
            # print link.text, sheet
            if sheet in link.text:
                # print link, type(link), link.text
                link.click()

    def overview_click(self):
        elem = self.driver.find_element_by_class_name('professions-tab')
        link = elem.find_element_by_tag_name('a')
        assert link
        # print link.text
        link.click()

    def profession_click(self, profession):
        '''update-content-professions-1
        class="professions-tab"
        '''
        elem = self.driver.find_element_by_id('update-content-professions-1')
        # print elem, type(elem), elem.text
        links = elem.find_elements_by_tag_name('a')
        assert links
        for link in links:
            # print link.text
            if profession in link.text:
                # print link, type(link), link.text
                link.click()

    def get_finished_tasks(self):
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "professions-slots"))
            )
        except:
            logger.log("element with class 'professions-slots' not found")
            return False
        '''
        .professions-slots > li:nth-child(1) > span:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(6) > button:nth-child(4)
        .professions-slots > li:nth-child(2) > span:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(6) > button:nth-child(4)
        .professions-slots > li:nth-child(5) > span:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(6) > button:nth-child(4)
        '''
        buttons = elem.find_elements_by_tag_name('button')
        # tasks_in_progress = [b for b in buttons if b.text == u'Завершить сейчас']
        tasks_finished = [b.click for b in buttons if b.text == u'Забрать результат']
        logger.log("tasks finished: %d" % len(tasks_finished))
        # print "tasks in progress:", len(tasks_in_progress)
        return tasks_finished


    def finish_task(self):
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "professions-rewards-modal"))
            )
        except:
            logger.log("element with class 'professions-rewards-modal' not found")
            return False
        # elem = self.driver.find_element_by_class_name('professions-rewards-modal')
        button = elem.find_element_by_tag_name('button')
        button.click()


    def get_free_slots(self):
        self.overview_click()
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "professions-slots"))
            )
        except:
            logger.log("element with class 'professions-slots' not found")
            return False
        buttons = elem.find_elements_by_tag_name('button')
        slots_free = [b.click for b in buttons if b.text == u'Выбрать поручение']
        logger.log("свободных слотов: %d" % len(slots_free))
        return slots_free


    def run_new_task(self, task):
        "http://gateway.nw.ru.perfectworld.eu/#char%28nick@email%29/professions-tasks/Leatherworking/Leatherworking_Tier3_Gather_Basic"
        logger.log(u"запускаю новую задачу - %s" % task)
        # widget_input = self.driver.find_element_by_tag_name('input')
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dataTables_filter"))
            )
        except:
            logger.log("element with class 'dataTables_filter' not found")
            return False
        widget_input = elem.find_element_by_tag_name('input')
        widget_input.clear()
        widget_input.send_keys(task + Keys.RETURN)
        time.sleep(5)
        table = self.driver.find_element_by_id('tasklist')
        button = table.find_element_by_tag_name('button')
        print button.text
        button.click()
        time.sleep(5)
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "box-footer"))
            )
        except:
            logger.log("element with class 'box-footer' not found")
            return False
        buttons = elem.find_elements_by_tag_name('button')
        for button in buttons:
            if button.text == u'Начать поручение':
                button.click()
        logger.log("задача запущена")
        time.sleep(5)
