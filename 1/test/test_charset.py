#!/usr/bin/env python
# coding: utf-8

import re
import sys

charset_rec = re.compile("<meta .*?charset *=.+?>")

def get_charset(content):
    mos = charset_rec.findall(content)
    for mo in mos:
        mos = re.compile("charset *=.+?\"").findall(mo)
        if mos:
            charset = mos[0].lstrip("charset").lstrip(' =')
            charset = charset.rstrip("/>").strip(' \'"')
            return charset
    return None

def charset_valid(charset):
    charsets = ['utf-8', 'gbk', 'gb2312', 'iso8859-1']
    return charset in charsets

def test_charset(contents):
    try:
        for content in contents:
            charset = get_charset(content).lower()
            valid = charset_valid(charset)
            print "{}: '{}' in '{}'".format(valid, charset, content)
    except:
        s = sys.exc_info()
        print "exception {0} happened on line {1}".format(s[1], s[2].tb_lineno)
        return s[1]

if __name__=="__main__":
    test_charset(['<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />',
                '<meta charset="UTF-8"/>',
                '<meta http-equiv="content-type" content="text/html; charset=utf-8" />',
                '<meta http-equiv="Content-type" content="text/html; charset=gb2312" />',
                '<meta http-equiv=Content-Type content="text/html;charset=utf-8">'
                ])