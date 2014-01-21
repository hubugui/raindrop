#!/usr/bin/env python
# coding: utf-8

import gzip, cStringIO
import HTMLParser
import urllib2
import web
import re
import sys

import dba

class FetchTask:
    '''
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <meta charset="utf-8">
        <title>Portal</title>
    '''
    def __init__(self):
        self.title_rec = re.compile("[^<!--]<title>([\s\S]*?)</title>")
        self.charset_rec = re.compile("<meta .*?charset *=.+?>")

    def get_title_from_content(self, content):
        mo = self.title_rec.search(content)
        if mo:            
            return mo.group(1).strip()
        return None

    def get_charset_from_content(self, content):
        mos = self.charset_rec.findall(content)
        for mo in mos:
            mos = re.compile("charset *=.+?\"").findall(mo)
            if mos:
                charset = mos[0].lstrip("charset").lstrip(' =')
                charset = charset.rstrip("/>").strip(' \'"')
                return charset.lower()
        return None

    def get_header_value(self, response, key):
        try:
            return response.headers[key]
        except:
            return None

    def POST(self):
        data = web.data()
        foo = data.split('-')
        if len(foo) > 1:
            id = int(foo[0])
            foo.remove(foo[0])
            url = '-'.join(foo)

            # mark fetch
            dba.msg_text_update_title_contet(id, u'标题抓取ing', '')

            try:
                response = urllib2.urlopen(url)
                content = response.read()

                print data
                print response.headers

                # http header->encoding
                encoding = self.get_header_value(response, 'Content-Encoding')
                if encoding == 'gzip':
                    content = gzip.GzipFile(fileobj = cStringIO.StringIO(content)).read()

                # http header->type
                charset = None
                ctype = self.get_header_value(response, 'Content-Type')
                if ctype:
                    # for example: text/html; charset=utf-8
                    ctype = ctype.lower().replace(' ', '').strip()
                    foo = ctype.split('text/html;charset=')
                    if len(foo) == 2 and len(foo[1]) > 0:
                        charset = foo[1]

                # http body->charset
                if charset is None:
                    charset = self.get_charset_from_content(content)
                if charset is None:
                    charset = 'gbk'

                # convert
                if charset <> 'utf-8':
                    print "unicode convert({})".format(charset)
                    content = unicode(content, charset)
                # update content
                dba.msg_text_update_title_contet(id, None, content)

                title = self.get_title_from_content(content)
                if title:
                    parser = HTMLParser.HTMLParser()
                    if charset == 'utf-8':
                        title = parser.unescape(title.decode('utf-8'))
                    else:
                        title = parser.unescape(title)
                else:
                    title = u'月亮吃标题'
                row_count, result = dba.msg_text_update_title_contet(id, title, '')
                return result
            except urllib2.HTTPError as e:
                return "{} {}, HTTP fetch failed".format(e.code, e.read)
            except:
                s = sys.exc_info()
                print "exception {0} happened on line {1}".format(s[1], s[2].tb_lineno)
                return s[1]
        else:
            return "'{}' is invalid format, right is '4366-http://yourdomain/a/0315.html'".format(data)

        return "OK"