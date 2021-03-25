from socketserver import BaseRequestHandler

from setting import HEADERS, HEADER_SIZE
from handle_processes import *


class RequestHandler(BaseRequestHandler):
    def handle(self):
        def select_process(header):
            if header not in HEADERS.values():
                return None
            else:
                return {HEADERS['RECORD']: SaveRecordProcess(request=self.request),
                        HEADERS['SHUTDOWN']: ShutDownProcess(server=self.server),
                        HEADERS['SAVE START']: SaveStartProcess(self.server, self.request),
                        HEADERS['SAVE STOP']: SaveStopProcess(self.server, self.request)}.get(header)

        msg_header = self.request.recv(HEADER_SIZE)
        process = select_process(msg_header)

        if process:
            process.execute()
        else:
            print('\nIncorrect header is given:', msg_header)
