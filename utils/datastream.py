from datetime import datetime
from struct import unpack_from, calcsize

import numpy as np

from setting import IS_PRINT, COLLECTING_DEVICE_MAC, SNIFFER_STATIONS


def parse_datastream(buffer):
    def unpacking(form):
        nonlocal offset
        unpacked = unpack_from(form, buffer, offset)[0]
        offset += calcsize(form)
        return unpacked

    def print_data():
        nonlocal timestamp, device_id, records

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
        records[mac] = rssi

    if IS_PRINT:
        print_data()

    try:
        record = records[COLLECTING_DEVICE_MAC]
    except KeyError:
        record = None

    return timestamp, device_id, record


def raw_to_fingerprint_pmc(raw_data):
    fp_dict = {}

    for device_id in SNIFFER_STATIONS:
        rssi_set = [rssi for _, rssi in raw_data[device_id]]
        fp_dict[device_id] = int(np.mean(rssi_set) if rssi_set else -99)

    return list(fp_dict.values())
