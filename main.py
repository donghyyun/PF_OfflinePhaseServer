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

while threading.active_count() > 1:
    time.sleep(3)
    print('\rCollected data size: {}'.format(len(DataList.instance())), end='')

server.server_close()
# server closed
print('server closed...')
