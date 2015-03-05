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

BASE_URL = "https://gateway.nw.ru.perfectworld.eu/"

nw = NW(BASE_URL, cookies)
time.sleep(2)
nw.login(useremail, password)
time.sleep(5)
nw.select_character(character_name)