from socketserver import ThreadingTCPServer
import threading

from RequestHandler import RequestHandler
from setting import SERVER_ADDRESS, CONSTRUCTION_TYPE


with ThreadingTCPServer(SERVER_ADDRESS, RequestHandler) as server:
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print('open server with {} method'.format(CONSTRUCTION_TYPE))

    while threading.active_count() > 1:
        pass

    print('-Active threads(In main)-\n', threading.enumerate())

print('\n\nserver closed...')
