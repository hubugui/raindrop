#!/usr/bin/env python
# coding: utf-8

from cron.PictureDay import *
from WXMessage import *

class WXMessageBuilder:
    def to_text(self, msgs, to_user, from_user, create_time):
        xml_string = u"<xml>\n" \
                        "<ToUserName><![CDATA[{}]]></ToUserName>\n" \
                        "<FromUserName><![CDATA[{}]]></FromUserName>\n" \
                        "<CreateTime><![CDATA[{}]]></CreateTime>\n" \
                        "<MsgType><![CDATA[{}]]></MsgType>\n" \
                        "<Content><![CDATA[{}]]></Content>\n" \
                    "</xml>"

        content = ""
        if len(msgs) > 0:
            for msg in msgs:
                content = content + msg['title'] + "\n"
                content = content + msg['content'] + "\n"
        else:
            content = u"哥们～我在[乒乓][啤酒]"
        return xml_string.format(to_user, from_user, create_time, "text", content)

    def to_news(self, msgs, to_user, from_user, create_time):
        xml_string = u"<xml>\n" \
                        "<ToUserName><![CDATA[{}]]></ToUserName>\n" \
                        "<FromUserName><![CDATA[{}]]></FromUserName>\n" \
                        "<CreateTime>{}</CreateTime>\n" \
                        "<MsgType><![CDATA[{}]]></MsgType>\n" \
                        "<ArticleCount>{}</ArticleCount>\n" \
                        "<Articles>\n" \
                            "{}\n" \
                        "</Articles>\n" \
                    "</xml>\n" \

        item_string = u"<item>\n" \
                        "<Title><![CDATA[{}]]></Title>\n" \
                        "<Description><![CDATA[{}]]></Description>\n" \
                        "<PicUrl><![CDATA[{}]]></PicUrl>\n" \
                        "<Url><![CDATA[{}]]></Url>\n" \
                        "</item>\n" \

        idx = 0                    
        content = ""
        for msg in msgs:
            pic_url = ""
            if idx == 0:
                pic_url = PictureDay.get_newest_url()
            idx = idx + 1

            content = content + item_string.format(msg['title'], '', pic_url, msg['content'])
        return xml_string.format(to_user, from_user, create_time, "news", len(msgs), content)

    def build(self, msgs, to_user, from_user, create_time):
        if len(msgs) > 0:
            return self.to_news(msgs, to_user, from_user, create_time)
        else:
            return self.to_text(msgs, to_user, from_user, create_time)