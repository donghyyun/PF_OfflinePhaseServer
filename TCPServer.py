from socketserver import BaseRequestHandler
import threading
from struct import calcsize

import datastream_processes as dp

STARTING_SYMBOL = b'RECORD'
MAX_LENGTH = 2048


class Handler(BaseRequestHandler):
    def handle(self):
        msg_header = self.request.recv(calcsize('6s'))
        print(msg_header)
        if msg_header == STARTING_SYMBOL:
            buffer = self.request.recv(MAX_LENGTH)

            p = threading.Thread(target=dp.process, args=(buffer,))
            p.start()

        elif msg_header == b'SHUTDW':
            print('STOP')
            # self.__setattr__(self.server, '_BaseServer')
        else:
            print('Incorrect entry string')
