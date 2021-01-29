import Setting
from Data import DBConnector, RawDataCollection

import socketserver, threading
from struct import calcsize
import datastream_processes as dp

HEADERS = {'RECORD': b'RECORD', 'SHUTDOWN': b'SHUTDW', 'SAVE START': b'SVSTRT', 'SAVE STOP': b'SVSTOP'}
MAX_LENGTH = 2048
LOCK = threading.Lock()


def threads_join():
    for thread in threading.enumerate():
        name = thread.getName()

        if name.startswith("Thread-") and thread is not threading.current_thread():
            # print(name, 'wait for close')
            thread.join()
            # print(name, 'is closed')


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        msg_header = self.request.recv(calcsize('6s'))

        process = {HEADERS['RECORD']: self.record_save_process,
                   HEADERS['SHUTDOWN']: self.shutdown_process,
                   HEADERS['SAVE START']: self.save_start_process,
                   HEADERS['SAVE STOP']: self.save_stop_process}.get(msg_header, self.shutdown_process)

        if msg_header not in HEADERS.values():
            process(msg_header)
        else:
            process()

    # Corresponding Processes
    def record_save_process(self):
        buffer = self.request.recv(MAX_LENGTH)
        timestamp, device_id, records = dp.parse_datastream(buffer)

        if len(records) == 1 and Setting.SAVE:
            LOCK.acquire()
            try:
                RawDataCollection.instance().add(timestamp, device_id, records[Setting.COLLECTING_DEVICE_MAC[0]])
            finally:
                LOCK.release()

    def shutdown_process(self, incorrect_header=None):
        self.server.shutdown()
        DBConnector.instance().close()
        threads_join()

        if incorrect_header:
            print("\nIncorrect header is given: ", incorrect_header, end="")
        print('\nshutdown:: shutdown_process')

    def save_start_process(self):
        self.server.shutdown()
        print('\nshutdown:: save_start_process')

        threads_join()
        Setting.SAVE = True

        coordinate = self.request.recv(10).decode()
        x, y = (int(i) for i in coordinate.split(','))
        print("Coordinate: ", x, y)
        DBConnector.instance().set_coordinate(x, y)

        print('reopen server at %s:: save_start_process' % threading.current_thread().getName())
        self.server.serve_forever()

    def save_stop_process(self):
        self.server.shutdown()
        print('\nshutdown:: save_stop_process')

        threads_join()
        Setting.SAVE = False

        # save to database
        # RawDataCollection.instance().print()
        DBConnector.instance().insert(RawDataCollection.instance().get())

        LOCK.acquire()
        try:
            RawDataCollection.instance().remove_all()
        finally:
            LOCK.release()

        print('reopen server at %s:: save_stop_process' % threading.current_thread().getName())
        self.server.serve_forever()
