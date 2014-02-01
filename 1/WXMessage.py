#!/usr/bin/env python
# coding: utf-8

import hashlib
import xml.etree.cElementTree as ET

class WXMessage:
    def __init__(self, to_user, from_user, create_time, msg_type, msg_id):
        self.to_user = to_user
        self.from_user = from_user
        self.create_time = create_time
        self.msg_type = msg_type
        self.msg_id = msg_id
        self.dicts = {"to_user":to_user, 
                    "from_user":from_user, 
                    "create_time":int(create_time), 
                    "msg_type":msg_type, 
                    "msg_id":int(msg_id)}

    def get_dicts(self):
        return self.dicts

class WXMessageEvent(WXMessage):
    def __init__(self, to_user, from_user, create_time, msg_type, event):
        WXMessage.__init__(self, to_user, from_user, create_time, msg_type, 0)
        self.event = event
        self.dicts["event"] = event

class WXMessageText(WXMessage):
    def __init__(self, to_user, from_user, create_time, msg_type, content, msg_id):
        WXMessage.__init__(self, to_user, from_user, create_time, msg_type, msg_id)
        self.content = content
        self.dicts["content"] = content

class WXMessageImage(WXMessage):
    def __init__(self, to_user, from_user, create_time, msg_type, pic_url, media_id, msg_id):
        WXMessage.__init__(self, to_user, from_user, create_time, msg_type, msg_id)
        self.pic_url = pic_url
        self.media_id = media_id

class WXMessageVoice(WXMessage):
    def __init__(self, to_user, from_user, create_time, msg_type, media_id, format, msg_id):
        WXMessage.__init__(self, to_user, from_user, create_time, msg_type, msg_id)
        self.media_id = media_id
        self.format = format

class WXMessageVideo(WXMessage):
    def __init__(self, to_user, from_user, create_time, msg_type, media_id, thumb_media_id, msg_id):
        WXMessage.__init__(self, to_user, from_user, create_time, msg_type, msg_id)
        self.media_id = media_id
        self.thumb_media_id = thumb_media_id

class WXMessageLocation(WXMessage):
    def __init__(self, to_user, from_user, create_time, msg_type, location_x, location_y, scale, label, msg_id):
        WXMessage.__init__(self, to_user, from_user, create_time, msg_type, msg_id)
        self.location_x = location_x
        self.location_y = location_y
        self.scale = scale
        self.label = label

class WXMessageLink(WXMessage):
    def __init__(self, to_user, from_user, create_time, msg_type, title, description, url, msg_id):
        WXMessage.__init__(self, to_user, from_user, create_time, msg_type, msg_id)
        self.title = title
        self.description = description
        self.url = url