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
        self.title_rec = re.compile("<title>([\s\S]*)</title>")
        self.charset_rec = re.compile("<meta .*?charset *=.+?>")

    def get_title(self, content):
        mo = self.title_rec.search(content)
        if mo:            
            return mo.group(1).strip()
        return None

    def get_charset(self, content):
        mos = self.charset_rec.findall(content)
        for mo in mos:
            mos = re.compile("charset *=.+?\"").findall(mo)
            if mos:
                charset = mos[0].lstrip("charset").lstrip(' =')
                charset = charset.rstrip("/>").strip(' \'"')
                return charset.lower()
        return None

    def POST(self):
        data = web.data()
        foo = data.split('-')
        if len(foo) > 1:
            id = int(foo[0])
            foo.remove(foo[0])
            url = '-'.join(foo)

            dba.msg_text_update_title_contet(id, u'标题抓取ing', '')

            try:
                response = urllib2.urlopen(url)
                content = response.read()

                print data
                print response.headers

                if 'Content-Encoding' in response.headers:
                    encoding = response.headers['Content-Encoding']
                else:
                    encoding = "none"
                if encoding == 'gzip':
                    content = gzip.GzipFile(fileobj = cStringIO.StringIO(content)).read()

                charset = self.get_charset(content)
                if charset is None:
                    charset = 'gbk'

                if charset <> 'utf-8':
                    print "unicode convert({})".format(charset)
                    content = unicode(content, charset)
                title = self.get_title(content)

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