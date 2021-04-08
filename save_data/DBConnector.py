from pymongo import MongoClient, DESCENDING
from threading import Lock
from .Singleton import Singleton
from setting import *


class DBConnector(metaclass=Singleton):
    def __init__(self):
        self._client = MongoClient(MONGO_HOST, MONGO_PORT)
        self._db = self._client[DB_NAME]

        self._lock = Lock()

    def __insert(self, collection_name, docs):
        if not docs:
            return None

        with self._lock:
            collection = self._db[collection_name]
            collection.insert(docs)

    def __find(self, collection_name, query):
        with self._lock:
            collection = self._db[collection_name]
            return collection.find(query)

    def __delete(self, collection_name, query):
        with self._lock:
            collection = self._db[collection_name]
            collection.delete_many(query)

    def insert_records(self, records):
        def document(timestamp_, rssi_):
            return {
                    'MAC': COLLECTING_DEVICE_MAC,
                    'rssi': rssi_,
                    'timestamp': timestamp_
                }

        for device_id in records.keys():
            docs = [document(timestamp, rssi) for timestamp, rssi in records[device_id]]
            self.__insert(PREFIX + device_id, docs)

    def insert_save_inform(self, coordinates_tup, timestamps):
        start, stop = timestamps
        doc = {
            'save_start_time': start,
            'save_stop_time': stop
        }

        try:
            from_x, from_y, to_x, to_y = coordinates_tup
            doc.update({
                'from_coordinate': [from_x, from_y],
                'to_coordinate': [to_x, to_y],
            })
        except ValueError:
            doc.update({
                'coordinate': coordinates_tup,
            })
        finally:
            self.__insert(SAVE_INFORM_NAME, doc)

    def insert_checkpoint(self):
        doc = {
            # 'device_id': SNIFFER_STATIONS[next(CHECKPOINTS)],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.__insert('checkpoints', doc)

    def insert_rm_point(self, coordinate, fp, num_each):
        if not fp:
            return

        doc = {
            "fingerprint": fp,
            "coordinate": coordinate,
            "DEBUG_num of collected rssi": num_each
        }
        self.__insert(RADIOMAP_NAME, doc)

    def delete_recent_data(self):
        docs = self.__find(SAVE_INFORM_NAME, {})
        recent_save_info = docs.sort('save_stop_time', DESCENDING).limit(1)[0]
        start_time, stop_time = recent_save_info['save_start_time'], recent_save_info['save_stop_time']

        query = {'$and': [{'timestamp': {'$gte': start_time}}, {'timestamp': {'$lte': stop_time}}]}
        for device_id in SNIFFER_STATIONS:
            self.__delete(PREFIX + device_id, query)

        self.__delete('checkpoints', query)
        self.__delete(SAVE_INFORM_NAME, {'_id': recent_save_info['_id']})

    def close(self):
        self._client.close()
