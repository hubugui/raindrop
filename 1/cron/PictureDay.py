#!/usr/bin/env python
# coding: utf-8

import datetime
import json
import urllib2
import random
import re
import sys
import web

sys.path.append("..")

import memcache_client

class PictureDay_Source:
	def get_newest_url(self):
		pass

class PictureDay_Source_Flickr(PictureDay_Source):
	def get_newest_url(self):
		result = None

		try:
			url = "http://api.flickr.com/services/feeds/groups_pool.gne?id=2334705@N25&format=json"
			content = urllib2.urlopen(url).read()

			# remove JS variable name
			content = content.strip()
			content = content[:-1]
			content = content.replace("jsonFlickrFeed(", "")

			# remove tab
			content = content.replace("\t", "")
			# remove descrption attribue
			rex = "\"description\": +\".+?\","
			content = re.compile(rex).sub('', content)

			# extract URL
			json_obj = json.loads(content)
			result = json_obj['items'][6]['media']['m']
		except:
			s = sys.exc_info()
			print "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)

		return result

class PictureDay_Source_NASA(PictureDay_Source):
	def get_newest_url(self, now=None):
		result = None

		try:
			if now is None:
				now = datetime.datetime.now() - datetime.timedelta(days=1)

			url = "http://apod.nasa.gov/apod/ap%02d%02d%02d.html" % (now.year % 1000, now.month, now.day)
			content = urllib2.urlopen(url).read()

			rex = "<img src=\"image/%02d%02d/.+?\"" % (now.year % 1000, now.month)
			mos = re.compile(rex, re.I).findall(content)
			if mos and len(mos) > 0:
				content = re.compile("<img src=\"", re.I).sub('', mos[0])
				content = content.replace("\"", '')
				result = "http://apod.nasa.gov/apod/{}".format(content)
			else:
				now = datetime.datetime.now() - datetime.timedelta(days=random.randint(2,1000))
				result = self.nasa_newest(default_url, now)
		except:
			s = sys.exc_info()
			print "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)

		return result

class PictureDay:
	default_newest_url = "http://apod.nasa.gov/apod/image/1312/lovejoy1_peach_960.jpg"

	@staticmethod
	def get_newest_url():
		if not memcache_client.mc.get('picture_of_day'):
			PictureDay.set_newest_url(default_newest_url)
		url = memcache_client.mc.get("picture_of_day")
		return url

	@staticmethod
	def set_newest_url(url):
		memcache_client.mc.set("picture_of_day", url)

	def GET(self):
		url = None
		wi = web.input()

		if 't' not in wi:
			source = PictureDay_Source_NASA()
			url = source.get_newest_url()
			if url:
				PictureDay.set_newest_url(url)
		url = PictureDay.get_newest_url()
		return url