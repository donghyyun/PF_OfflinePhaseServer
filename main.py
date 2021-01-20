from TCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler
from Setting import HOST, PORT
from DataList import DataList
import threading, time

# run server and saving the data
server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
print('open server')

while server_thread.is_alive() or threading.active_count() > 1:
    time.sleep(3)
    if server_thread.is_alive():
        print('\rCollected data size: {}'.format(len(DataList.instance())), end='')
    else:
        print()

server.server_close()
# server shut down

# data to fingerprint (t, r1, r2, r3, ...)
print('Collected Data')
print('=' * 50)
DataList.instance().print()
