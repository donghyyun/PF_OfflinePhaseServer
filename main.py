from socketserver import ThreadingTCPServer
import threading

from RequestHandler import RequestHandler
from setting import SERVER_ADDRESS


with ThreadingTCPServer(SERVER_ADDRESS, RequestHandler) as server:
    threading.Thread(target=server.serve_forever, daemon=False).start()
    print('open server')

    while threading.active_count() > 1:
        pass

    print('-Active threads(In main)-\n', threading.enumerate())

print('\n\nserver closed...')
