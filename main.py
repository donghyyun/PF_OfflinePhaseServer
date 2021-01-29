from TCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler, LOCK
from Setting import HOST, PORT
from Data import RawDataCollection

import threading, time

# run server and saving the data
server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
print('open server')

while threading.active_count() > 1:
    time.sleep(3)

    LOCK.acquire()
    try:
        print('\rCollected data size: {}'.format(len(RawDataCollection.instance())), end='')
    finally:
        LOCK.release()


server.server_close()
# server closed
print('\nserver closed...')
