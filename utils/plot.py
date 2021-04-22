import numpy as np
from matplotlib import pyplot as plt


def plot_rss_trend(device_id, records):
    records = np.array(records)
    time_list, rssi_list = records[:, 0], records[:, 1]
    plt.plot(time_list, rssi_list)
    plt.scatter(time_list, rssi_list)
    plt.title(device_id)
    plt.show()