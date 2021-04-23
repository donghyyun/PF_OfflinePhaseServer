import multiprocessing
import time
from socketserver import ThreadingTCPServer
import threading

from RequestHandler import RequestHandler
from setting import SERVER_ADDRESS, CONSTRUCTION_TYPE, print_settings


if __name__ == '__main__':
    print_settings()

    with ThreadingTCPServer(SERVER_ADDRESS, RequestHandler) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print('open server with {} method'.format(CONSTRUCTION_TYPE))

        while threading.active_count() > 1:
            time.sleep(2)

        print('-Active threads(In main)-\n', threading.enumerate())

    print('\n\nserver closed...')
    while not multiprocessing.Queue.empty():
        print(multiprocessing.Queue.g)
