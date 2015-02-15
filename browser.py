#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'yorick'

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from log import log

class NW():
    def __init__(self, base_url, cookies):
        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Firefox()
        self.driver.get('https://gateway.nw.ru.perfectworld.eu/faq.html')
        log("page loaded")
        # chrome_options = Options()
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

    def select_character(self, select_char_name):

        elem = self.driver.find_element_by_class_name('content_title')
        assert 'Выбор персонажа' in elem.text

        elem = self.driver.find_element_by_class_name('charselect')
        char_list = elem.find_elements_by_class_name('char-list-name')
        assert char_list is not None
        for char_name in char_list:
            print char_name

