from .Singleton import Singleton
from threading import Lock
from setting import SNIFFER_STATIONS


class RawDataCollection(metaclass=Singleton):
    def __init__(self):
        self.data_dict = {}
        self.x, self.y = 0, 0
        for device_id in SNIFFER_STATIONS:
            self.data_dict[device_id] = []

        self._lock = Lock()

    def count_each(self):
        return [len(self.data_dict[_id]) for _id in self.data_dict.keys()]

    def set_coordinate(self, x, y):
        self.x, self.y = x, y

    def add(self, timestamp, device_id, rssi):
        with self._lock:
            self.data_dict[device_id].append((timestamp, rssi))

    def remove_all(self):
        for _id in self.data_dict.keys():
            self.data_dict[_id].clear()

    def print(self):
        self._sort()
        for _id in self.data_dict.keys():
            print('>' + _id, len(self.data_dict[_id]))
            for record in self.data_dict[_id]:
                print(record)
            print()

    def _sort(self):
        for _id in self.data_dict.keys():
            self.data_dict[_id].sort(key=lambda x: x[0])

    def get(self):
        self._sort()
        return self.data_dict, self.x, self.y
