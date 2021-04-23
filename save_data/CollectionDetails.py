from collections import OrderedDict
from datetime import datetime

from threading import Lock
from setting import SNIFFER_STATIONS

lock = Lock()


class CollectionDetails:
    def __init__(self):
        self.record_dict = OrderedDict()
        for device_id in SNIFFER_STATIONS:
            self.record_dict[device_id] = 0

        self.__coordinate = None
        self.__save_start_time = None
        self.__save_stop_time = None

    @property
    def coordinate(self):
        return self.__coordinate

    @coordinate.setter
    def coordinate(self, coordinate_tup):
        self.__coordinate = coordinate_tup

    @property
    def save_start_time(self):
        return self.__save_start_time

    @save_start_time.setter
    def save_start_time(self, time=None):
        if type(time) is datetime:
            self.__save_start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.__save_start_time = time

    @property
    def save_stop_time(self):
        return self.__save_stop_time

    @save_stop_time.setter
    def save_stop_time(self, time=None):
        if type(time) is datetime:
            self.__save_stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.__save_stop_time = time

    def record_count(self):
        return list(self.record_dict.values())

    def increase_count(self, device_id):
        with lock:
            self.record_dict[device_id] += 1

    def clear(self):
        for _id in self.record_dict.keys():
            self.record_dict[_id] = 0

        self.__coordinate = None
        self.__save_start_time = None
        self.__save_stop_time = None

    def print(self):
        print(self.record_dict.items())
