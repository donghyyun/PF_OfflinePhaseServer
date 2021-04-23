from threading import Lock

from pymongo import MongoClient

from save_data.Singleton import Singleton
from setting import MONGO_HOST, MONGO_PORT, DB_NAME


class DBConnector(metaclass=Singleton):
    __client = MongoClient(MONGO_HOST, MONGO_PORT)
    __db = __client[DB_NAME]
    __lock = Lock()

    @property
    def db(self):
        return DBConnector.__db

    @property
    def lock(self):
        return DBConnector.__lock

    def close(self):
        self.__del__()

    def __del__(self):
        self.__client.close()

