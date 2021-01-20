import Setting


class DataList:
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
        self.data_dict = {}
        for device_id in Setting.sniffer_stations:
            self.data_dict[device_id] = []

    def __len__(self):
        return sum(len(self.data_dict[_id]) for _id in self.data_dict.keys())

    def add(self, timestamp, device_id, rssi):
        self.data_dict[device_id].append((timestamp, rssi))

    def print(self):
        self.__sort()
        for _id in self.data_dict.keys():
            print('>' + _id)
            for record in self.data_dict[_id]:
                print(record)
            print()

    def __sort(self):
        for _id in self.data_dict.keys():
            self.data_dict[_id].sort(key=lambda x: x[0])

    def get(self):
        return self.data_dict
