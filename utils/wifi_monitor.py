from datetime import datetime, timedelta

from setting import LAST_CONNECTION_TIME

LOST, UNSTABLE, NTP_ERROR = 'Lost', 'Unstable', 'NTP error'


def get_state(now, last_time):
    last_time = datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
    if last_time.year < now.year:
        return NTP_ERROR
    if last_time + timedelta(seconds=10) < now:
        return LOST
    if last_time + timedelta(seconds=5) < now:
        return UNSTABLE
    return None


def print_connection_state():
    now = datetime.now()
    connection_states = {LOST: [], UNSTABLE: [], NTP_ERROR: []}
    print('>>>connection_states at ', now.strftime('%Y-%m-%d %H:%M:%S'))

    for device_id in LAST_CONNECTION_TIME.keys():
        state = get_state(now, LAST_CONNECTION_TIME[device_id])
        if state:
            connection_states[state].append(device_id)

    if not sum(connection_states.values(), []):
        print("All monitors' connections are good\n")
        return None

    for key in connection_states.keys():
        if connection_states[key]:
            print('\t' + key + ':', connection_states[key])
    print()


if __name__ == '__main__':
    import time

    while True:
        try:
            time.sleep(2)
            print_connection_state()
        except KeyboardInterrupt:
            print('Keyboard interrupted')
            break
