from pymongo import DESCENDING

from .DBConnector import DBConnector
from setting import *


class DeleteDBConnector(DBConnector):
    def __find(self, collection_name, query):
        if not query:
            raise Exception('query is not given')

        with self.lock:
            collection = self.db[collection_name]
            return collection.find(query)

    def find_recent_collection_detail(self):
        docs = self.__find(COLLECTION_DETAILS_NAME, {})
        return docs.sort('save_start_time', DESCENDING).limit(1)[0]

    def __delete(self, collection_name, query=None):
        if not query:
            raise Exception('query is not given')

        with self.lock:
            collection = self.db[collection_name]
            collection.delete_many(query)

    def delete_records(self, query=None):
        for device_id in SNIFFER_STATIONS:
            self.__delete(PREFIX + device_id, query)

    def delete_collection_detail(self, query=None):
        self.__delete(COLLECTION_DETAILS_NAME, query)

    def delete_checkpoints(self, query=None):
        self.__delete('checkpoints', query)

    def delete_recent_data(self):
        recent_info = self.find_recent_collection_detail()
        start_time, stop_time = recent_info[START_TIME], recent_info[STOP_TIME]

        query = {'$and': [{TIMESTAMP: {'$gte': start_time}}, {TIMESTAMP: {'$lte': stop_time}}]}

        self.delete_records(query)
        self.delete_checkpoints(query)
        self.delete_collection_detail({'_id': recent_info['_id']})
