__author__ = 'yorick'
from selenium import webdriver

BASE_URL = "http://gateway.nw.ru.perfectworld.eu/"

browser = webdriver.Chrome()
browser.get(BASE_URL)
