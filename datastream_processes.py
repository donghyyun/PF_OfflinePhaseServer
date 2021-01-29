from struct import calcsize, unpack_from
from datetime import datetime
from Setting import COLLECTING_DEVICE_MAC, PRINT, sniffer_stations

import numpy as np


def parse_datastream(buffer):
    def unpacking(form):
        nonlocal offset
        unpacked = unpack_from(form, buffer, offset)[0]
        offset += calcsize(form)
        return unpacked

    def print_data():
        nonlocal timestamp, device_id, records
        if not records:
            return

        string = '[%s] [%s] - %d records\n' % (timestamp, device_id, len(records))
        for _mac in records.keys():
            string += _mac + '(%s) ' % (records[_mac])
        print(string)

    offset = 0
    id_len = unpacking('B')
    device_id = unpacking(str(id_len) + 's').decode()

    unix_time = unpacking('>q')
    timestamp = datetime.fromtimestamp(unix_time / 1000).strftime('%Y-%m-%d %H:%M:%S')

    records = {}
    record_len = unpacking('>H')
    for _ in range(record_len):
        mac = unpacking('6s').hex().upper()
        rssi = -1 * unpacking('B')

        if COLLECTING_DEVICE_MAC is None or mac in COLLECTING_DEVICE_MAC:
            records[mac] = rssi

    if PRINT:
        print_data()

    return timestamp, device_id, records


def raw_to_fingerprint_pmc(collection):
    fp_dict = {}

    for device_id in sniffer_stations:
        rss = [record[1] for record in collection[device_id]]
        fp_dict[device_id] = int(np.mean(rss) if rss != [] else -999)

    return list(fp_dict.values())

