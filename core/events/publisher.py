import zmq
from django.conf import settings

from ..common import Singleton


class Publisher(metaclass=Singleton):
    """
    Publisher is singleton which sends updates to all services.

    Only sending Parking lots currently implemented.
    """

    def __init__(self):
        port = settings.env.str('ZMQ_PUB_PORT')
        self._ctx = zmq.Context()
        self._socket = self._ctx.socket(zmq.PUB)
        self._socket.bind(f'tcp://*:{port}')

    def send_parking_lots(self, parking_site_id, parking_lots):
        self._socket.send(f'parking-{parking_site_id}_'.encode('utf-8'), flags=zmq.SNDMORE)
        self._socket.send_pyobj(parking_lots)
