from socketserver import BaseRequestHandler
import threading
from struct import calcsize

import datastream_processes as dp

STARTING_SYMBOL = b'RECORD'
MAX_LENGTH = 2048


class Handler(BaseRequestHandler):
    def handle(self):
        if self.request.recv(calcsize('6s')) == STARTING_SYMBOL:
            buffer = self.request.recv(MAX_LENGTH)

            p = threading.Thread(target=dp.process, args=(buffer,))
            p.start()

        else:
            print('Incorrect entry string')
