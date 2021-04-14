import abc
import threading

from save_data import InsertDBConnector, RecordCollection


class AbstractProcess:
    __is_save = False
    __db_connector = InsertDBConnector()
    __record_collection = RecordCollection()

    def __init__(self, server=None, request=None):
        self.server = server
        self.request = request

    @property
    def db_connector(self):
        return AbstractProcess.__db_connector

    @property
    def record_collection(self):
        return AbstractProcess.__record_collection

    @property
    def is_save(self):
        return AbstractProcess.__is_save

    @is_save.setter
    def is_save(self, boolean):
        AbstractProcess.__is_save = boolean

    @abc.abstractmethod
    def execute(self):
        pass

    def shutdown_and_wait(self):
        self.server.shutdown()
        self.record_processes_join()

    def reopen_server(self, process_name=''):
        self.set_thread_name("REOPEN")
        print('\t-Active threads( In', process_name, ')-\n\t', self.get_active_threads())
        print('<<<' + process_name + ':: reopen server at', threading.current_thread())
        self.server.serve_forever()

    def send_msg_to_client(self, msg):
        try:
            self.request.send(msg.encode())
        except Exception as e:
            print(e, '\nerror to send', msg)

    @staticmethod
    def get_active_threads():
        threads = []
        for thread in threading.enumerate():
            if thread.name.startswith('Main') or thread.name.startswith('pymongo'):
                continue
            threads.append(thread)

        return threads

    @staticmethod
    def set_thread_name(name):
        thread = threading.current_thread()
        thread.name = name + " " + thread.name

    @staticmethod
    def record_processes_join():
        for thread in threading.enumerate():
            name = thread.getName()

            if name.startswith("RECORD"):
                thread.join()
