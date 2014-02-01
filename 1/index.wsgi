import os

import sae
import web
import dba

from WX import *
from WXService import *

from cron.PictureDay import *
from task.FetchTask import *
from memcache_client import *

urls = (
    '/', 'Index',
    '/wx', 'WX',
    '/cron/pictureday', 'PictureDay',
    '/task/fetch', 'FetchTask'
)

class Index:
    def GET(self):
        return render.index()

# templates
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

# memcahce
memcache_client.initialize()

# database
dba.db = web.database(dbn='mysql', 
                    host=sae.const.MYSQL_HOST,
                    port=int(sae.const.MYSQL_PORT),
                    user=sae.const.MYSQL_USER, 
                    pw=sae.const.MYSQL_PASS, 
                    db=sae.const.MYSQL_DB)

# weixin
WX.wxs = WXService()

# webpy
app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)