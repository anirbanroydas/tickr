import tornado.web
import tornado.escape
import logging


LOGGER = logging.getLogger(__name__)


# Handles the general HTTP connections
class TickrApiHandler(tornado.web.RequestHandler):
    """This handler is a basic regular HTTP handler to serve the tickr requests.

    """

    def prepare(self):
        
        self.rabbitmq = self.application.rabbitmq_client



    def post(self):
        """
        This method is called when a client does a simple POST request,
        all other HTTP requests like GET, PUT, DELETE, etc are ignored.

        :return: Returns a success message as soon as the received payload is published to rabbitmq
        """

        LOGGER.info('[TickrApiHandler] HTTP connection opened')

        # process the message received
        msg = self.process_tickr_message()

        # channel wher to publish, may be public or specific client_id
        publish_to_channel = msg['channel'] if 'channel' in msg else 'public'
        
        # publish message to rabbitmq
        status = 200
        message = 'Tickr Message published succesfully'

        if publish_to_channel:
            routing_key = 'tickr.{0}.*'.format(publish_to_channel)

            LOGGER.info('[TickrApiHandler] routing_key : {0}'.format(routing_key))

            try:
                self.rabbitmq.publish(msg, routing_key)

            except Exception as e:
                LOGGER.error("Exception Caused while publishing to RabbitMq for msg : ", msg)
                LOGGER.error("Exception  : ", e)
                status = 500
                message = 'Tickr Message Not Pusblised due to Server Error'
        

        res = {
            'status': status,
            'message': message
        }

        self.set_status(status, reason=message)
        self.write(res)




    def process_tickr_message(self):
        """
        This method processes the post payload received.
        
        :param      self     The object
        
        :return:     Returns the  message that needs to be published to the tickr exchange of rabbitmq.

        """

        msg = tornado.escape.json_decode(self.request.body)
        LOGGER.info(self.request.body)
        LOGGER.info(msg)

        return msg








