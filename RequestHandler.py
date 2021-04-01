from socketserver import BaseRequestHandler

from setting import HEADERS, HEADER_SIZE
from handle_processes import *


class RequestHandler(BaseRequestHandler):
    def handle(self):
        def select_process(header):
            if header not in HEADERS.values():
                return None

            return {HEADERS['RECORD']: SaveRecordProcess,
                    HEADERS['SHUTDOWN']: ShutDownProcess,
                    HEADERS['SAVE START']: SaveStartProcess,
                    HEADERS['SAVE STOP']: SaveStopProcess,
                    HEADERS['CHECKPOINT']: MarkCheckpointProcess}.get(header)

        msg_header = self.request.recv(HEADER_SIZE)
        process = select_process(msg_header)

        if process:
            process(self.server, self.request).execute()
        else:
            print('\nIncorrect header is given:', msg_header)
