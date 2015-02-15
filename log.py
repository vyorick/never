#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'yorick'

import time


class log():
    def __init__(self):
        self.timer = time.time()


    def log(self, msg):
        print ""