import numpy as np

from utils.datetime import time_diff
from save_data import FindDBConnector
from setting import START_POINT, STOP_POINT, START_TIME, STOP_TIME


class CollectedDetails:
    def __init__(self, detail_name):
        self.detail_name = detail_name

        self.start_point = None
        self.stop_point = None
        self.start_time = None
        self.stop_time = None

        self.angle = None
        self.collection_time = None
        self.distance = None

    def set_details(self, idx):
        info = FindDBConnector().find_recent(self.detail_name, key='save_start_time', idx=idx)

        self.start_point, self.stop_point = np.array(info[START_POINT]), np.array(info[STOP_POINT])
        self.start_time, self.stop_time = info[START_TIME], info[STOP_TIME]

        self.angle = self.calculate_angle()
        self.collection_time = time_diff(self.stop_time, self.start_time)
        self.distance = np.linalg.norm(self.stop_point - self.start_point)

    def calculate_angle(self):
        def to_radian(angle):
            return angle * np.pi / 180.0

        from_x, from_y = self.start_point
        to_x, to_y = self.stop_point

        if to_x == from_x:
            if to_y == from_y:
                return None
            if to_y > from_y:
                return to_radian(90)
            return to_radian(-90)

        if to_y == from_y and to_x < from_x:
            return to_radian(180)

        return np.arctan((to_y - from_y) / (to_x - from_x))
