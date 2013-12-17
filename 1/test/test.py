#!/usr/bin/env python
# coding: utf-8

import re
import socket
import urllib2
import json
import sys

def test_flickr_picture_json():
    yaho_pic_day_newest_url = ''

    try:
        yaho_pic_day_url_json = "http://api.flickr.com/services/feeds/groups_pool.gne?id=2334705@N25&format=json"
        response = urllib2.urlopen(yaho_pic_day_url_json)
        content = response.read()

        # remove JS variable name
        content = content.strip()
        content = content[:-1]
        content = content.replace("jsonFlickrFeed(", "")

        print 1

        # remove tab
        content = content.replace("\t", "")
        # remove descrption attribue
        rex = "\"description\": +\".+?\","
        content = re.compile(rex).sub('', content)

        print 2

        json_obj = json.loads(content)
        tmp = json_obj['items'][0]['media']['m']
        print 3
        if yaho_pic_day_newest_url == tmp:
            yaho_pic_day_newest_url = json_obj['items'][1]['media']['m']
        else:
            yaho_pic_day_newest_url = tmp
        print 4
    except:
        s = sys.exc_info()
        print "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
    
    print yaho_pic_day_newest_url

def setup_http_proxy():
    ipaddr = socket.gethostbyname(socket.gethostname())
    if ipaddr.index('137.') == 0:
        opener = urllib2.build_opener(urllib2.ProxyHandler({'http': '10.77.8.70:8080', 'https':'10.77.8.70:8080'}))
        urllib2.install_opener(opener)

def test_url(url):
    response = urllib2.urlopen(url)
    content = response.read()
    print content

if __name__=="__main__":
    setup_http_proxy()

    # test_WXMessage()
    # test_FetchTask("")
    # test_flickr_picture_json()
    test_url(sys.argv[1])