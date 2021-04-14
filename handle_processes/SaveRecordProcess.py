import abc

from setting import LAST_CONNECTION_TIME
from .AbstractProcess import AbstractProcess
from . import _datastream_processes as dp

MAX_LENGTH = 2048


class SaveRecordProcess(AbstractProcess):
    @abc.abstractmethod
    def execute(self):
        buffer = self.request.recv(MAX_LENGTH)
        timestamp, device_id, record = dp.parse_datastream(buffer)
        LAST_CONNECTION_TIME[device_id] = timestamp

        if not self.is_save or not record:
            return None

        self.set_thread_name("RECORD")
        self.record_collection.add(timestamp, device_id, record)
        self.db_connector.insert_one(timestamp, device_id, record)
