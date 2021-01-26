from pymongo import MongoClient
import Setting


class DBConnector:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls.__getInstance
        return cls.__instance

    def __init__(self):
        self.client = MongoClient(Setting.MONGO_HOST, Setting.MONGO_PORT)
        db = self.client[Setting.DB_NAME]
        self.collection = db[Setting.COLLECTION_NAME]

    def insert(self, data_dict):
        for _id in data_dict.keys():
            doc = {
                "device_id": _id,
                "records": data_dict[_id]
            }
            self.collection.insert(doc)

    def close(self):
        self.client.close()

