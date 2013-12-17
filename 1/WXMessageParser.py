#!/usr/bin/env python
# coding: utf-8

import xml.etree.cElementTree as ET

from WXMessage import *

class WXMessageParser:
    def extract_string(self, root, tag):
        return root.iter(tag).next().text.strip()

    def parse(self, data):
        msg = None

        root = ET.fromstring(data)

        to_user = self.extract_string(root, 'ToUserName')
        from_user = self.extract_string(root, 'FromUserName')
        create_time = self.extract_string(root, 'CreateTime')
        msg_type = self.extract_string(root, 'MsgType')

        msg_type = msg_type.lower()

        if msg_type == 'event':
            event = self.extract_string(root, 'Event')
            msg = WXMessageEvent(to_user, from_user, create_time, msg_type, event)
        elif msg_type == "text":
            msg_id = self.extract_string(root, 'MsgId')
            content = self.extract_string(root, 'Content')
            msg = WXMessageText(to_user, from_user, create_time, msg_type, content, msg_id)
        elif msg_type == "image":
            msg_id = self.extract_string(root, 'MsgId')
            pic_url = self.extract_string(root, 'PicUrl')
            media_id = self.extract_string(root, 'MediaId')
            msg = WXMessageImage(to_user, from_user, create_time, msg_type, pic_url, media_id, msg_id)
        elif msg_type == "voice":
            msg_id = self.extract_string(root, 'MsgId')
            media_id = self.extract_string(root, 'MediaId')
            format = self.extract_string(root, 'Format')
            msg = WXMessageVoice(to_user, from_user, create_time, msg_type, media_id, format, msg_id)
        elif msg_type == "video":
            msg_id = self.extract_string(root, 'MsgId')
            media_id = self.extract_string(root, 'MediaId')
            thumb_media_id = extract_string(root, 'ThumbMediaId')
            msg = WXMessageVideo(to_user, from_user, create_time, msg_type, media_id, thumb_media_id, msg_id)
        elif msg_type == "location":
            msg_id = self.extract_string(root, 'MsgId')
            location_x = self.extract_string(root, 'Location_X')
            location_y = self.extract_string(root, 'Location_Y')
            scale = self.extract_string(root, 'Scale')
            label = self.extract_string(root, 'Label')
            msg = WXMessageLocation(to_user, from_user, create_time, msg_type, location_x, location_y, scale, label, msg_id)
        elif msg_type == "link":
            msg_id = self.extract_string(root, 'MsgId')
            title = self.extract_string(root, 'Title')
            description = self.extract_string(root, 'Description')
            url = self.extract_string(root, 'Url')
            msg = WXMessageLink(to_user, from_user, create_time, msg_type, title, description, url, msg_id)
        else:
            pass

        return msg