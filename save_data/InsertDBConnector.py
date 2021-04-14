from .DBConnector import DBConnector

from setting import *


class InsertDBConnector(DBConnector):
    def __insert(self, collection_name, docs=None):
        if not docs:
            raise Exception('docs are empty')

        with self._lock:
            collection = self._db[collection_name]
            collection.insert(docs)

    def insert_one(self, timestamp, device_id, record):
        doc = {
            'MAC': COLLECTING_DEVICE_MAC,
            'rssi': record,
            'timestamp': timestamp
        }
        self.__insert(PREFIX + device_id, doc)

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
            self.__insert(SAVE_INFORM_NAME, doc)
        except ValueError:
            # PMC case
            return None

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

    def rename_collection(self, old_name, new_name):
        with self._lock:
            self._db[old_name].rename(new_name)
