import abc
import threading
import time

from save_data import DBConnector, RawDataCollection
from setting import COLLECTING_DEVICE_MAC, CONSTRUCTION_TYPE
from handle_processes import _datastream_processes as dp

MAX_LENGTH = 2048


def record_processes_join():
    for thread in threading.enumerate():
        name = thread.getName()

        if name.startswith("RECORD"):
            thread.join()


class AbstractProcess:
    _is_save = False

    def __init__(self, server=None, request=None):
        self._server = server
        self._request = request

        self._db_connector = DBConnector()
        self._raw_data_collection = RawDataCollection()

    @classmethod
    def is_save(cls):
        return cls._is_save

    @classmethod
    def set_save(cls, boolean):
        cls._is_save = boolean

    @abc.abstractmethod
    def execute(self):
        pass

    def reopen_server(self, process_name=''):
        # print('-Active threads( In', process_name, ')-\n', threading.enumerate())
        print('reopen server at %s' % threading.current_thread().getName())
        self._server.serve_forever()

    def send_msg_to_device(self, msg):
        try:
            self._request.send(msg.encode())
        except Exception as e:
            print(e, '\nerror to send', msg)


class ShutDownProcess(AbstractProcess):
    @abc.abstractmethod
    def execute(self):
        print('\n>>>shutdown process::', threading.current_thread())

        self._server.shutdown()
        self._db_connector.close()
        record_processes_join()

        # Just for debugging
        print('-Active threads(In shutdown process)-\n', threading.enumerate())


class SaveRecordProcess(AbstractProcess):
    def _save_raw_data(self, timestamp, device_id, record):
        if CONSTRUCTION_TYPE == 'PMC':
            self._raw_data_collection.add(timestamp, device_id, record)
        elif CONSTRUCTION_TYPE == 'WS':
            self._db_connector.insert_raw(timestamp, device_id, record)

    @abc.abstractmethod
    def execute(self):
        buffer = self._request.recv(MAX_LENGTH)
        timestamp, device_id, records = dp.parse_datastream(buffer)

        current_thread = threading.current_thread()
        current_thread.name = "RECORD " + current_thread.getName()

        if AbstractProcess.is_save():
            try:
                record = records[COLLECTING_DEVICE_MAC]
            except KeyError:
                record = -99
            finally:
                self._save_raw_data(timestamp, device_id, record)


class SaveStartProcess(AbstractProcess):
    def run_pmc_process(self, buffer):
        x, y, collect_time = (int(i) for i in buffer.split(','))

        self._raw_data_collection.set_coordinate(x, y)
        self.send_msg_to_device("Saving start-coordinate: (%d, %d)\n"
                                "collect time: %d" % (x, y, collect_time))

        threading.Thread(target=self.reopen_server,
                         args=('save_start_process',)).start()

        time.sleep(collect_time)
        SaveStopProcess(self._server, self._request).execute()

    def run_ws_process(self, buffer):
        pass

    @abc.abstractmethod
    def execute(self):
        print('\n>>>save_start_process', threading.current_thread())

        self._server.shutdown()
        record_processes_join()
        AbstractProcess.set_save(True)

        buffer = self._request.recv(100).decode().strip()

        # need to check format of buffer
        if CONSTRUCTION_TYPE == 'PMC':
            self.run_pmc_process(buffer)

        elif CONSTRUCTION_TYPE == 'WS':
            # mark saving start timestamp & collecting path or else
            pass


class SaveStopProcess(AbstractProcess):
    def run_pmc_process(self):
        raw_data, x, y = self._raw_data_collection.get()
        num_each = self._raw_data_collection.count_each()

        w_buffer = str(num_each) + "\n"

        if min(num_each) >= 2:
            fp = dp.raw_to_fingerprint_pmc(raw_data)
            print("fingerprint at" + "({}, {}):".format(x, y), fp, end="\t")
            print("collected size:", num_each)
            self._db_connector.insert_rm_point((x, y), fp, num_each)

            w_buffer += str(fp)
        else:
            w_buffer += "Not enough raw data"

        self._raw_data_collection.remove_all()
        return w_buffer

    def run_ws_process(self):
        pass

    @abc.abstractmethod
    def execute(self):
        print('\n>>>save_stop_process', threading.current_thread())

        self._server.shutdown()
        record_processes_join()
        AbstractProcess.set_save(False)

        # save to database
        if CONSTRUCTION_TYPE == 'PMC':
            w_buffer = self.run_pmc_process()
        elif CONSTRUCTION_TYPE == 'WS':
            self.run_ws_process()

        self.send_msg_to_device(w_buffer)
        threading.Thread(target=self.reopen_server,
                         args=('save_stop_process',)).start()
