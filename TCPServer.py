import socketserver, threading, Setting
from struct import calcsize
import datastream_processes as dp
from DataList import DataList
from DBConnector import DBConnector

HEADERS = {'RECORD': b'RECORD', 'SHUTDOWN': b'SHUTDW', 'SAVE START': b'SVSTRT', 'SAVE STOP': b'SVSTOP'}
MAX_LENGTH = 2048


def threads_join():
    for thread in threading.enumerate():
        if thread not in [threading.main_thread(), threading.current_thread()]:
            # print(thread.getName(), 'wait for close')
            thread.join()
            # print(thread.getName(), 'is closed')


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        msg_header = self.request.recv(calcsize('6s'))

        if msg_header == HEADERS['SHUTDOWN']:
            self.server.shutdown()
            DBConnector.instance().close()
            threads_join()

            print('\nshutdown server')
            return

        if msg_header not in HEADERS.values():
            print('Incorrect header is given: {}'.format(msg_header))
            return

        if msg_header == HEADERS['SAVE STOP']:
            self.server.shutdown()
            print('\nshutdown to stop saving')

            threads_join()
            Setting.SAVE = False

            # save to database
            # DataList.instance().print()
            DBConnector.instance().insert(DataList.instance().get())
            DataList.instance().remove_all()

            print('reopen server after saving to database at ', threading.current_thread().getName())
            self.server.serve_forever()

        elif msg_header == HEADERS['SAVE START']:
            self.server.shutdown()
            print('\nshutdown to start saving')

            # for PMC
            # coordinate = self.request.recv(10).decode()
            # x, y = coordinate.split(',')

            threads_join()
            Setting.SAVE = True

            print('reopen with start saving at ', threading.current_thread().getName())
            self.server.serve_forever()

        elif msg_header == HEADERS['RECORD']:
            buffer = self.request.recv(MAX_LENGTH)
            timestamp, device_id, records = dp.parse_datastream(buffer)

            if len(records) == 1 and Setting.SAVE:
                Setting.LOCK.acquire()
                try:
                    dp.save_data(timestamp, device_id, records)
                finally:
                    Setting.LOCK.release()

