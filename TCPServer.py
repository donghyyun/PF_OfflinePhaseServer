import socketserver, threading
from struct import calcsize
import datastream_processes as dp

STARTING_SYMBOL = b'RECORD'
SHUTDOWN_SYMBOL = b'SHUTDW'
MAX_LENGTH = 2048


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        msg_header = self.request.recv(calcsize('6s'))

        if msg_header == SHUTDOWN_SYMBOL:
            self.server.shutdown()

            for thread in threading.enumerate():
                if thread.getName() != 'MainThread' and thread is not threading.current_thread():
                    thread.join()

            print('\nshutdown server')

        elif msg_header == STARTING_SYMBOL:
            buffer = self.request.recv(MAX_LENGTH)
            dp.save_data(buffer)

        else:
            print('Incorrect entry string: ' + msg_header)
