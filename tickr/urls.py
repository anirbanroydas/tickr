from tornado import web
from tornado.web import URLSpec as url

from config.settings import settings
from lib.utils import include


urls = [
    url(r"/static/(.*)", web.StaticFileHandler,
        {"path": settings.get('static_path')}),
]
urls += include(r"/", "routes.tickrApi")
