import abc

from setting import LAST_CONNECTION_TIME
from .AbstractProcess import AbstractProcess
from utils.datastream import parse_datastream
from utils.threads import set_thread_name

MAX_LENGTH = 2048


class SaveRecordProcess(AbstractProcess):
    @abc.abstractmethod
    def execute(self):
        buffer = self.request.recv(MAX_LENGTH)
        timestamp, device_id, record = parse_datastream(buffer)
        LAST_CONNECTION_TIME[device_id] = timestamp

        if not self.is_save or not record:
            return None

        set_thread_name("RECORD")
        self.collection_details.increase_count(device_id)
        self.db_connector.insert_one(timestamp, device_id, record)
