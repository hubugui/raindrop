#!/usr/bin/env python
# coding: utf-8

import sys
import hashlib
import web

from WXService import *

wxs = None

class WX:
    request_keys = ['signature', 'timestamp', 'nonce', 'echostr']

    def input_valid(self, wi):
        for i in range(len(self.request_keys)):
        	if self.request_keys[i] not in wi:
        		return False, "parameter not enough, '{}' cannot be empty.".format(self.request_keys[i])
        return True, 'OK'

    def GET(self):
        wi = web.input()

        valid, result = self.input_valid(wi)
        if valid == True:
            result = WX.wxs.verify(wi["signature"], wi["timestamp"], wi["nonce"], wi["echostr"])
        return result

    def POST(self):
        wi = web.input()
        data = web.data()
        id, result = WX.wxs.process_message(data)
        return result