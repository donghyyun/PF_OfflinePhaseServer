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
        self.x, self.y = 0, 0

    def set_coordinate(self, x, y):
        self.x, self.y = x, y

    def insert(self, data_dict):
        for _id in data_dict.keys():
            doc = {
                "x": self.x,
                "y": self.y,
                "device_id": _id,
                "records": [record[1] for record in data_dict[_id]]
            }
            self.collection.insert(doc)

    def close(self):
        self.client.close()

