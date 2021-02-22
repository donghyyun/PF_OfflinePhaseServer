from pymongo import MongoClient
import Setting


class SingletonInstance:
    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls):
        cls.__instance = cls()
        cls.instance = cls.__get_instance
        return cls.__instance


class DBConnector(SingletonInstance):
    def __init__(self):
        self.client = MongoClient(Setting.MONGO_HOST, Setting.MONGO_PORT)
        self.db = self.client[Setting.DB_NAME]

    def insert_raw(self, raw_data):
        for device_id in Setting.SNIFFER_STATIONS:
            collection = self.db[device_id]
            docs = []
            for data in raw_data[device_id]:
                timestamp, rssi = data
                docs.append({
                    "MAC": Setting.COLLECTING_DEVICE_MAC,
                    "rssi": rssi,
                    "timestamp": timestamp
                })
            if docs:
                collection.insert_many(docs)

    def insert_rm_point(self, coordinate, fp, num_each):
        if not fp:
            return

        x, y = coordinate
        doc = {
                "fingerprint": fp,
                "coordinate": (x, y),
                "DEBUG_num of collected rssi": num_each
        }
        collection = self.db[Setting.RADIOMAP_NAME]
        collection.insert(doc)

    def find(self, query={}, fields={"_id": 0}):
        return [doc for doc in self.collection.find(query, fields)]

    def close(self):
        self.client.close()


class RawDataCollection(SingletonInstance):
    def __init__(self):
        self.data_dict = {}
        self.x, self.y = 0, 0
        for device_id in Setting.SNIFFER_STATIONS:
            self.data_dict[device_id] = []

    def __len__(self):
        return sum(len(self.data_dict[_id]) for _id in self.data_dict.keys())

    def count_each(self):
        return [len(self.data_dict[_id]) for _id in self.data_dict.keys()]

    def set_coordinate(self, x, y):
        self.x, self.y = x, y

    def add(self, timestamp, device_id, rssi):
        self.data_dict[device_id].append((timestamp, rssi))

    def remove_all(self):
        for _id in self.data_dict.keys():
            self.data_dict[_id].clear()

    def print(self):
        self.__sort()
        for _id in self.data_dict.keys():
            print('>' + _id, len(self.data_dict[_id]))
            for record in self.data_dict[_id]:
                print(record)
            print()

    def __sort(self):
        for _id in self.data_dict.keys():
            self.data_dict[_id].sort(key=lambda x: x[0])

    def get(self):
        self.__sort()
        return self.data_dict, self.x, self.y
