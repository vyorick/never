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


        # links = elem.find_elements_by_tag_name('a')
        # print links, type(links)
        '''
        char_list = self.driver.find_elements_by_class_name('char-list-name')
        assert char_list is not None
        print char_list, type(char_list)
        for char_name in char_list:
            logger.log(char_name)
        '''
