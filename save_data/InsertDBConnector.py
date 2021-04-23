from .DBConnector import DBConnector

from setting import *


class InsertDBConnector(DBConnector):
    def __insert(self, collection_name, docs=None):
        if not docs:
            raise Exception('docs are empty')

        with self.lock:
            collection = self.db[collection_name]
            collection.insert(docs)

    def insert_one(self, timestamp, device_id, record):
        doc = {
            MAC: COLLECTING_DEVICE_MAC,
            RSSI: record,
            TIMESTAMP: timestamp
        }
        self.__insert(PREFIX + device_id, doc)

    def insert_records(self, records):
        def document(timestamp_, rssi_):
            return {
                    MAC: COLLECTING_DEVICE_MAC,
                    RSSI: rssi_,
                    TIMESTAMP: timestamp_
                }

        for device_id in records.keys():
            docs = [document(timestamp, rssi) for timestamp, rssi in records[device_id]]
            self.__insert(PREFIX + device_id, docs)

    def insert_collection_details(self, collection_details):
        doc = {
            START_TIME: collection_details.save_start_time,
            STOP_TIME: collection_details.save_stop_time
        }

        try:
            from_x, from_y, to_x, to_y = collection_details.coordinate
            doc.update({
                START_POINT: [from_x, from_y],
                STOP_POINT: [to_x, to_y],
            })
        except ValueError:
            # PMC case
            x, y = collection_details.coordinate
            doc.update({
                POINT: [x, y]
            })
        finally:
            self.__insert(COLLECTION_DETAILS_NAME, doc)

    def insert_checkpoint(self):
        doc = {
            # 'device_id': SNIFFER_STATIONS[next(CHECKPOINTS)],
            TIMESTAMP: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.__insert('checkpoints', doc)

    def insert_rm_point(self, coordinate, fp, num_each):
        if not fp:
            return

        doc = {
            FINGERPRINT: fp,
            POINT: coordinate,
            "DEBUG_num of collected rssi": num_each
        }
        self.__insert(RADIOMAP_NAME, doc)

    def rename_collection(self, old_name, new_name):
        with self.lock:
            self.db[old_name].rename(new_name)
