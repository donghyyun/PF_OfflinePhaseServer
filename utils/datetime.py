from datetime import datetime


def time_diff(end_time, start_time):
    def to_datetime(strtime):
        return datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')

    start_time, end_time = to_datetime(start_time), to_datetime(end_time)

    if start_time > end_time:
        start_time, end_time = end_time, start_time

    return (end_time - start_time).seconds