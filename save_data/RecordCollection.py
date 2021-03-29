from datetime import datetime

from .Singleton import Singleton
from threading import Lock
from setting import SNIFFER_STATIONS


class RecordCollection(metaclass=Singleton):
    def __init__(self):
        self.record_dict = {}
        for device_id in SNIFFER_STATIONS:
            self.record_dict[device_id] = []

        self.coordinates = None
        self.save_start_time = None
        self.save_stop_time = None

        self._lock = Lock()

    def set_coordinates(self, coordinates_tup):
        self.coordinates = coordinates_tup

    def set_start_time(self):
        self.save_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def set_stop_time(self):
        self.save_stop_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def add(self, timestamp, device_id, rssi):
        with self._lock:
            self.record_dict[device_id].append((timestamp, rssi))

    def remove_records(self):
        for _id in self.record_dict.keys():
            self.record_dict[_id].clear()

    def print(self):
        for _id in self.record_dict.keys():
            print('>' + _id, len(self.record_dict[_id]))
            for record in self.record_dict[_id]:
                print(record)
            print()
