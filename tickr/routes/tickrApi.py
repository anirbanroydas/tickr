from tornado.web import URLSpec as url
from tickr.controllers.tickrHandler import TickrApiHandler

urls = [
    url(r"/api/v1/tickr", TickrApiHandler),
]

