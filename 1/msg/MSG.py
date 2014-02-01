import sys
import web

import dba

class MSG:
    request_keys = ['id']

    def input_valid(self, wi):
        for i in range(len(self.request_keys)):
            if self.request_keys[i] not in wi:
                return False, "parameter not enough, '{}' cannot be empty.".format(self.request_keys[i])
        return True, 'OK'

    def GET(self):
        wi = web.input()

        valid, result = self.input_valid(wi)
        if valid == True:
            result = dba.msg_text_query_id(int(wi["id"]))
        return result