#!/usr/bin/env python
# coding: utf-8
# File: WXFavWord.py  本日热词实现
# Author: Zelor Chang

import datetime

class WXFavWord:
    def FindIn(self, data):
        fw = u"无"
        array = [ u"哈哈", u"坑爹", u"无聊", u"有趣", u"类似" ]
        ind = int (int(data) % ( len(array) ) )
        fw = array[ ind ]
        return fw


## test unit
# now = datetime.datetime.now()
# test_favw = WXFavWord()
# fw = test_favw.FindIn( int(now) )
# print fw

