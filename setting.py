# server, sniffer_stations
SERVER_ADDRESS = ("143.248.55.136", 36918)
SNIFFER_STATIONS = ['DV101', 'DV102', 'DV103', 'DV104']

HEADERS = {'RECORD': b'RECORD', 'SHUTDOWN': b'SHUTDW', 'SAVE START': b'SVSTRT', 'SAVE STOP': b'SVSTOP'}
HEADER_SIZE = 6

COLLECTING_DEVICE_MAC = '08AED61A3E47'
IS_PRINT = False

CONSTRUCTION_TYPE = 'PMC'  # or 'WS': Walking Survey

# Database related var
MONGO_HOST, MONGO_PORT = "143.248.56.66", 19191
DB_NAME = "passive_fingerprint_dh"
RADIOMAP_NAME = 'test'  # "testpoint_N1_7F_half(ss4)"
