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

        if name.startswith("RECORD"):
            print(name, 'wait for close')
            thread.join()
            print(name, 'is closed')


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        msg_header = self.request.recv(calcsize('6s'))
        # print(threading.current_thread().getName(), msg_header)

        process = {HEADERS['RECORD']: self.record_save_process,
                   HEADERS['SHUTDOWN']: self.shutdown_process,
                   HEADERS['SAVE START']: self.save_start_process}.get(msg_header, self.shutdown_process)

        if msg_header not in HEADERS.values():
            process(msg_header)
        else:
            process()

    # Corresponding Processes
    def record_save_process(self):
        buffer = self.request.recv(MAX_LENGTH)
        timestamp, device_id, records = dp.parse_datastream(buffer)

        if Setting.SAVE and len(records) == 1:
            threading.current_thread().setName("RECORD" + threading.current_thread().getName())

            print(threading.current_thread().getName(), "wait for LOCK")
            LOCK.acquire()
            try:
                RawDataCollection.instance().add(timestamp, device_id, records[Setting.COLLECTING_DEVICE_MAC])
            finally:
                print(threading.current_thread().getName(), 'released LOCK')
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
        print('\n>>>save_start_process')

        Setting.SAVE = True

        buffer = self.request.recv(100).decode().strip()
        x, y, collect_time = (int(i) for i in buffer.split(','))

        RawDataCollection.instance().set_coordinate(x, y)
        self.request.send(("Saving start-coordinate: (%d, %d)" % (x, y)).encode())

        threading.Timer(collect_time, self.save_stop_process).start()

        print('reopen server at %s:: save_start_process' % threading.current_thread().getName())
        self.server.serve_forever()

    def save_stop_process(self):
        print('\n>>>save_stop_process')

        Setting.SAVE = False
        threads_join()

        # save to database
        raw_data, x, y = RawDataCollection.instance().get()
        fp = dp.raw_to_fingerprint_pmc(raw_data)
        num_each = RawDataCollection.instance().count_each()

        print("fingerprint at" + "({}, {}):".format(x, y), fp, end="\t")
        print("collected size:", num_each)
        DBConnector.instance().insert_rm_point((x, y), fp, num_each)
        DBConnector.instance().insert_raw(raw_data)

        RawDataCollection.instance().remove_all()

        self.request.send((str(fp) + "\n" + str(num_each)).encode())

        print('<<<save_stop_process')
