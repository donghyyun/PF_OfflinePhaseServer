from pymongo import MongoClient
from threading import Lock
from .Singleton import Singleton
from setting import MONGO_HOST, MONGO_PORT, DB_NAME, RADIOMAP_NAME, SNIFFER_STATIONS, COLLECTING_DEVICE_MAC


class DBConnector(metaclass=Singleton):
    def __init__(self):
        self._client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self._client[DB_NAME]

        self._lock = Lock()

    # def insert_raw(self, raw_data):
    #     for device_id in SNIFFER_STATIONS:
    #         collection = self.db[device_id]
    #         docs = []
    #         for data in raw_data[device_id]:
    #             timestamp, rssi = data
    #             docs.append({
    #                 "MAC": COLLECTING_DEVICE_MAC,
    #                 "rssi": rssi,
    #                 "timestamp": timestamp
    #             })
    #         if docs:
    #             collection.insert_many(docs)

    def insert_raw(self, timestamp, device_id, record):
        with self._lock:
            collection = self.db[device_id]
            collection.insert({
                'MAC': COLLECTING_DEVICE_MAC,
                'rssi': record,
                'timestamp': timestamp
            })

    def insert_rm_point(self, coordinate, fp, num_each):
        if not fp:
            return

        doc = {
                "fingerprint": fp,
                "coordinate": coordinate,
                "DEBUG_num of collected rssi": num_each
        }
        with self._lock:
            collection = self.db[RADIOMAP_NAME]
            collection.insert(doc)

    def close(self):
        self._client.close()
