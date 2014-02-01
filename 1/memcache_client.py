#!/usr/bin/env python
# coding: utf-8

import pylibmc as memcache

mc = None

def initialize():
	global mc
	mc = memcache.Client()

def finalize():
	global mc
	mc = None