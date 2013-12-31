#!/usr/bin/env python
# coding: utf-8

import datetime
import hashlib
import HTMLParser
import time
import xml.etree.cElementTree as ET

from sae.taskqueue import Task, TaskQueue
from sae.taskqueue import add_task

import dba

from WXMessageParser import *
from WXMessageBuilder import *
from WXFavWord import *

class WXService:
    def __init__(self):
        self.token = "hunshuibainianguorenjianyixing"
        self.msg_parser = WXMessageParser()
        self.msg_builder = WXMessageBuilder()
        self.msg_favword = WXFavWord()

    def verify(self, signature, timestamp, nonce, echostr):
        result = "parameter invalid"

        if signature and timestamp and nonce and echostr:
            # merge
            array = [self.token, timestamp, nonce]
            array.sort()
            content = reduce(lambda x, y : x + y, array)   

            # sha1
            m = hashlib.sha1()
            m.update(content)
            digest = m.hexdigest()
            if signature == digest:
                result = echostr
            else:
                result = "signature={} invalid".format(signature)

        return result

    def get_zero_ytc(self, dtime, hour):
        zero_str = "{}-{}-{} {}:{}:{}".format(dtime.year, dtime.month, dtime.day, hour, 0, 0)
        zero_time = time.strptime(zero_str, '%Y-%m-%d %H:%M:%S')
        return int(time.mktime(zero_time))

    # subscribe and unsubscribe
    def on_event(self, msg):
        msgs = None
        if "subscribe" == msg.event:
            text = u"欢迎关注！\n\n这里分享的内容主要是挨踢、八卦、历史、科学。\n\n"
            text = text + u"由于微信未向普通订阅号/开发者模式公开每日群发图文消息的机制，所以请发送\"i\"来获取最新内容！\n\n"
            text = text + u"忆从樊口载春酒，步上西山寻野梅。\n"
            text = text + u"●苏东坡《武昌西山》"
            msgs = [{'title':text, 'content':''}]
        elif "unsubscribe" == msg.event:
            text = u"再见!"
            msgs = [{'title':text, 'content':''}]
        else:
            return -1, "post data is wrong"
        return 0, self.msg_builder.to_text(msgs, msg.from_user, msg.to_user, int(time.time()))

    # URL
    def on_url(self, msg):
        text = None
        msgs = None
        id, result = dba.msg_text_insert(msg)
        print "id", id
        if id > 0:
            text = u"谢谢投递！"
            url = u"{}-{}".format(str(id), msg.content)
            add_task('FetchJobQueue', '/task/fetch', url)
        else:
            text = u"数据库操作不幸失败鸟！"
        msgs = [{'title':text, 'content':''}]
        return 0, self.msg_builder.to_text(msgs, msg.from_user, msg.to_user, int(time.time()))

    # command text
    def on_command(self, msg):
        now = datetime.datetime.now()
        cmd = msg.content
        offset_day = 0

        try:
            offset_day = int(cmd)
        except:
            offset_day = 0 

        if cmd in ('i', 'I'):
            yday = now - datetime.timedelta(days=1)

            # yestoday
            begin = self.get_zero_ytc(yday, 0)
            end = self.get_zero_ytc(now, 0)
            msgs = dba.msg_text_query_time(begin, end).list()
            return 0, self.msg_builder.build(msgs, msg.from_user, msg.to_user, int(time.time()))
        elif '0' == cmd:
            tday = now + datetime.timedelta(days=1)

            # today
            begin = self.get_zero_ytc(now, 0)
            end = self.get_zero_ytc(tday, 0)
            msgs = dba.msg_text_query_time(begin, end).list()
            return 0, self.msg_builder.build(msgs, msg.from_user, msg.to_user, int(time.time()))
        elif cmd in ('h', 'H'):
            text = u"发送URL投稿，发送i获取最新内容，发送-1获取前日内容，依此类推。"
            msgs = [{'title':text, 'content':''}]
            return 0, self.msg_builder.to_text(msgs, msg.from_user, msg.to_user, int(time.time()))
        elif cmd in ('v', 'V'):
            text = u"樊口的行板  版本号：ver:0.0.0.1 update131213。"
            msgs = [{'title':text, 'content':''}]
            return 0, self.msg_builder.to_text(msgs, msg.from_user, msg.to_user, int(time.time()))
        elif cmd in ('f', 'F'):
            begin = self.get_zero_ytc(now, 0)
            fw = self.msg_favword.FindIn( int(begin) )
            text = u"今日热词：" + fw
            msgs = [{'title':text, 'content':''}]
            return 0, self.msg_builder.to_text(msgs, msg.from_user, msg.to_user, int(time.time()))
        elif offset_day < 0:
            begin_day = now - datetime.timedelta(days=abs(offset_day-1))
            end_day = now - datetime.timedelta(days=abs(offset_day))

            # past day
            begin = self.get_zero_ytc(begin_day, 0)
            end = self.get_zero_ytc(end_day, 0)
            msgs = dba.msg_text_query_time(begin, end).list()
            return 0, self.msg_builder.build(msgs, msg.from_user, msg.to_user, int(time.time()))
        else:
            result = "unsupport"
            return -1, result

    # process wechat's message
    def process_message(self, data):
        msg = self.msg_parser.parse(data)
        if msg is None:
            return -1, "post data is wrong"

        if isinstance(msg, WXMessageEvent):
            return self.on_event(msg)
        elif isinstance(msg, WXMessageText):
            if msg.content.startswith("http://"):
                return self.on_url(msg)
            return self.on_command(msg)
        else:
            pass
        return -1, "post data unsupport"