import abc

from setting import COLLECTING_DEVICE_MAC
from .AbstractProcess import AbstractProcess
from . import _datastream_processes as dp

MAX_LENGTH = 2048


class SaveRecordProcess(AbstractProcess):
    def __save_raw_data(self, timestamp, device_id, record):
        self.record_collection.add(timestamp, device_id, record)
        # self.db_connector.insert_one(timestamp, device_id, record)

    @abc.abstractmethod
    def execute(self):
        buffer = self.request.recv(MAX_LENGTH)
        timestamp, device_id, records = dp.parse_datastream(buffer)

        if not self.is_save:
            return None

        self.set_thread_name("RECORD")

        # currently only one device is support to collect
        if COLLECTING_DEVICE_MAC in records.keys():
            self.__save_raw_data(timestamp, device_id, records[COLLECTING_DEVICE_MAC])
