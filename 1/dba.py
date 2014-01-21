#!/usr/bin/env python
# coding: utf-8

import os
import sys
import datetime

from WXMessage import *

db = None

def msg_text_insert(msg):
    try:
        dicts = msg.get_dicts()
        id = db.insert('message_text', **dicts)
        if id > 0:
            return id, "OK"
        else:
            return id, "database cannot insert row"
    except:
        s = sys.exc_info()
        print "exception {0} happened on line {1}".format(s[1], s[2].tb_lineno)
        return -1, s[1]

def msg_text_update(id, msg):
    try:
        dicts = msg.get_dicts()
        row_count = db.update('message_text', where='id={}'.format(id, **dicts))
        if row_count > 0:
            return row_count, "OK"
        else:
            return row_count, "message id={} no exist".format(id)
    except:
        s = sys.exc_info()
        print "exception {0} happened on line {1}".format(s[1], s[2].tb_lineno)
        return -1, s[1]

def msg_text_update_title_contet(id, title, content):
    try:
        dicts = {}
        if title:
            dicts['title'] = title
        if content:
            dicts['text'] = content
        if len(dicts) > 0:
            row_count = db.update('message_text', where='id={}'.format(id), **dicts)
            if row_count > 0:
                return row_count, "OK"
            else:
                return row_count, "message id={} no exist".format(id)
        else:
            return 0, "parameters is None"
    except:
        s = sys.exc_info()
        print "exception {0} happened on line {1}".format(s[1], s[2].tb_lineno)
        return -1, s[1]    

def msg_text_delete(id):
    try:
        row_count = db.delete('message_text', where='id=$id', vars=locals())
        if row_count > 0:
            return row_count, "OK"
        else:
            return row_count, "message id={} no exist".format(id)
    except:
        s = sys.exc_info()
        print "exception {0} happened on line {1}".format(s[1], s[2].tb_lineno)
        return -1, s[1]

def msg_text_query_id(id):
    try:
        return db.select('message_text', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def msg_text_query_time(begin, end):
    try:
        return db.select('message_text', 
                        where="create_time >= {} and create_time < {}".format(begin, end),
                        what="content,title", 
                        limit="0,10",
                        order="id",
                        group="content,title")
    except IndexError:
        return None