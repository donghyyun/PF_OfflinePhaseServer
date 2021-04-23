from collections import OrderedDict

import numpy as np

from save_data import FindDBConnector
from setting import SNIFFER_STATIONS, PREFIX, PERIOD, TIMESTAMP, RSSI
from utils.datetime import time_diff


class WSCollectedDetails:
    def __init__(self, details):
        self.start_time = details.save_start_time
        self.stop_time = details.save_stop_time

        self.start_point = np.array(details.coordinate[:2])
        self.stop_point = np.array(details.coordinate[2:])

        self.angle = self.calculate_angle()
        self.collection_time = time_diff(self.stop_time, self.start_time)
        self.distance = np.linalg.norm(self.stop_point - self.start_point)

    def calculate_angle(self):
        def to_radian(angle):
            return angle * np.pi / 180.0

        from_x, from_y = self.start_point
        to_x, to_y = self.stop_point

        if to_x == from_x:
            if to_y == from_y:
                return None
            if to_y > from_y:
                return to_radian(90)
            return to_radian(-90)

        if to_y == from_y and to_x < from_x:
            return to_radian(180)

        return np.arctan((to_y - from_y) / (to_x - from_x))

    def continuous_rss_list(self, record_set):
        record_dict = {
            time_diff(record[TIMESTAMP], self.start_time): int(record[RSSI])
            for record in record_set
        }

        continuous_record = OrderedDict()
        for t in range(self.collection_time):
            try:
                continuous_record[t] = record_dict[t]
            except KeyError:
                continuous_record[t] = -99

        return list(continuous_record.values())

    def get_batch_record_list(self):
        db_connector = FindDBConnector()
        query = {
            '$and': [
                {TIMESTAMP: {'$gte': self.start_time}},
                {TIMESTAMP: {'$lte': self.stop_time}}
            ]
        }

        batch_record_list = []
        for ss in SNIFFER_STATIONS:
            record_set = list(db_connector.find_sorted(PREFIX + ss, query, key=TIMESTAMP))
            batch_record_list.append(
                self.continuous_rss_list(record_set)
            )

        db_connector.close()
        return batch_record_list

    def to_fingerprints(self):
        batch_record_list = self.get_batch_record_list()

        fingerprints = []
        for t in range(0, self.collection_time, PERIOD):
            fingerprints.append(
                [max(records[t: t + PERIOD]) for records in batch_record_list]
            )

        return fingerprints
