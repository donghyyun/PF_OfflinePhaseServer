import numpy as np

from save_data import FindDBConnector
from setting import SNIFFER_STATIONS, PREFIX, TIMESTAMP, RSSI
from utils.datetime import time_diff


class PMCCollectedDetails:
    def __init__(self, details):
        self.start_time = details.save_start_time
        self.stop_time = details.save_stop_time

        self.point = details.coordinate
        self.collection_time = time_diff(self.stop_time, self.start_time)

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
                [record[RSSI] for record in record_set]
            )

        db_connector.close()
        return batch_record_list

    def to_fingerprints(self):
        batch_record_list = self.get_batch_record_list()
        fingerprints = [int(np.mean(record_list)) for record_list in batch_record_list]

        return fingerprints
