#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'yorick'

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from log import log

logger = log()


class NW():
    def __init__(self, base_url, cookies):
        self.driver = webdriver.Firefox()
        self.driver.get('https://gateway.nw.ru.perfectworld.eu/faq.html')
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

    def select_character(self, char_name):
        logger.log("page: " + self.driver.title)
        assert u'Выбор персонажа' in self.driver.title
        time.sleep(5)
        elem = self.driver.find_element_by_class_name('charselect')
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
        <div class="button-list">
            <a class="nav-button mainNav dungeons nav-dungeons" data-url="#char(Yorick@vyorick)/adventures"></a>
            <a class="nav-button mainNav charactersheet nav-charsheet" data-url="#char(Yorick@vyorick)/charactersheet"></a>
            <a class="nav-button mainNav inventory nav-inventory" data-url="#char(Yorick@vyorick)/inventory"></a>
            <a class="nav-button mainNav professions nav-professions" data-url="#char(Yorick@vyorick)/professions"></a>
            <a class="nav-button mainNav auctionhouse nav-auction" data-url="#char(Yorick@vyorick)/auctionhouse"></a>
            <a class="nav-button mainNav exchange nav-exchange" data-url="#char(Yorick@vyorick)/exchange"></a>
            <a class="nav-button mainNav zenmarket nav-zenmarket" data-url="#char(Yorick@vyorick)/zenmarket"></a>
            <a class="nav-button mainNav guild nav-guild" data-url="#guild(%D0%A1%D1%83%D0%BF%D0%B5%D1%80%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8B)"></a>
            <a class="nav-button mainNav mail nav-mail" data-url="#char(Yorick@vyorick)/mail"></a>
        </div>
        '''
        logger.log("page: " + self.driver.title)
        assert u'Портал Neverwinter' in self.driver.title
        elem = self.driver.find_element_by_class_name('button-list')
        # print elem, type(elem), elem.text
        links = elem.find_elements_by_tag_name('a')
        assert links
        for link in links:
            # print link.text, sheet
            if sheet in link.text:
                # print link, type(link), link.text
                link.click()

