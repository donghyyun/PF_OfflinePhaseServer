from collections import OrderedDict

from utils.datetime import time_diff
from save_data import FindDBConnector
from setting import PREFIX, SNIFFER_STATIONS, PERIOD


class CollectedRecords:
    def __init__(self, details):
        self.details = details
        self.start_time = details.start_time
        self.stop_time = details.stop_time

        self.batch_record_list = self.get_batch_record_list()

    def continuous_rss_list(self, record_set):
        record_dict = {
            time_diff(record['timestamp'], self.start_time): int(record['rssi'])
            for record in record_set
        }

        continuous_record = OrderedDict()
        for t in range(self.details.collection_time):
            try:
                continuous_record[t] = record_dict[t]
            except KeyError:
                continuous_record[t] = -99

        return list(continuous_record.values())

    def get_batch_record_list(self):
        db_connector = FindDBConnector()
        query = {
            '$and': [
                {'timestamp': {'$gte': self.start_time}},
                {'timestamp': {'$lte': self.stop_time}}
            ]
        }

        batch_record_list = []
        for ss in SNIFFER_STATIONS:
            record_set = list(FindDBConnector().find_sorted(PREFIX + ss, query, key='timestamp'))
            batch_record_list.append(
                self.continuous_rss_list(record_set)
            )

        db_connector.close()
        return batch_record_list

    def to_fingerprints(self):
        fingerprints = []
        for t in range(0, self.details.collection_time, PERIOD):
            fingerprints.append(
                [max(records[t: t + PERIOD]) for records in self.batch_record_list]
            )

        return fingerprints
