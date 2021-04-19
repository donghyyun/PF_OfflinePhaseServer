from pymongo import DESCENDING, ASCENDING

from .DBConnector import DBConnector


class FindDBConnector(DBConnector):
    def find_recent(self, collection_name, key='_id', idx=0):
        with self.lock:
            return self.db[collection_name].find().sort(key, DESCENDING).limit(idx + 1)[idx]

    def find_sorted(self, collection_name, query={}, key='_id'):
        with self.lock:
            return self.db[collection_name].find(query).sort(key, ASCENDING)
