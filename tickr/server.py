import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.options import define, options
import logging
import time

from lib import utils
from urls import urls
from config.settings import settings

from tickr.lib.pubsub import RabbitMqClient


define("port", default=7001, help="run on the given port", type=int)

LOGGER = logging.getLogger(__name__)


class Application(tornado.web.Application):

    def __init__(self, rabbitmq_client):

        tornado.web.Application.__init__(self, urls, **settings)

        # Initialize new pika rabbitmq client object for this websocket.
        self.rabbitmq_client = rabbitmq_client
        


def main():
    tornado.options.parse_command_line()

    rabbitmq_client = RabbitMqClient(
                                    queue='tickr-queue-' + utils.genid(16),
                                    only_publish=True,
                                    exchange='tickr_exchange',
                                    exchange_type='topic',
                                    exchange_durability=True,
                                    queue_binding_key='tickr.*.*',
                                    queue_durability=True,
                                    queue_exclusivity=True,
                                    queue_auto_delete=True
                                )

    app = Application(rabbitmq_client)
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)

    LOGGER.info('[server.main] Starting server on port : %s', options.port)

    try:
        LOGGER.info("\n[server.main] Server Started.\n")

        ioloop = tornado.ioloop.IOLoop.current()
        # connect to rabbitmq
        ioloop.add_timeout(time.time() + 1, rabbitmq_client.start)

        # start ioloop
        ioloop.start()
        
    except KeyboardInterrupt:
        LOGGER.error('\n[server.main] EXCEPTION KEYBOARDINTERRUPT INITIATED\n')
        LOGGER.info("[server.main] Stopping Server....")
        LOGGER.info('[server.main] closing all websocket connections objects and corresponsding pika client objects')
        LOGGER.info("\n[server.main] Server Stopped.")

        # Stopping main thread's ioloop, not to be confused with current thread's ioloop
        # which is ioloop.IOLoop.current()
        tornado.ioloop.IOLoop.instance().stop()

        LOGGER.info("\n[server.main] Elaster server Stopped.")


if __name__ == "__main__":
    main()
