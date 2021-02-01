from TCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler
from Setting import SERVER_HOST, SERVER_PORT, SNIFFER_STATIONS
from Data import RawDataCollection

import threading, time

# run server and saving the data
server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
print('open server')

prev_count = [0 for _ in SNIFFER_STATIONS]
while threading.active_count() > 1:
    time.sleep(3)

    current_count = RawDataCollection.instance().count_each()
    if prev_count != current_count:
        print('\rCollected data size: ', current_count, end='')
        prev_count = current_count


server.server_close()
# server closed
print('\nserver closed...')
