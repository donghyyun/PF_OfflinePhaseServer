import abc
import threading
import time

from setting import PMC_MIN_FP
from .AbstractProcess import AbstractProcess
from . import _datastream_processes as dp


class SaveStopProcess(AbstractProcess):
    @staticmethod
    def __is_enough_records(record_count):
        if min(record_count) < PMC_MIN_FP:
            return False
        return True

    @staticmethod
    def __is_pmc_construction(coordinates):
        if len(coordinates) == 2:
            return True
        return False

    @abc.abstractmethod
    def execute(self):
        self.set_thread_name("SAVE_STOP")
        print('\n>>>save_stop_process', threading.current_thread())

        self.record_collection.set_stop_time()
        time.sleep(1)

        self.shutdown_and_wait()
        self.is_save = False

        record_dict = self.record_collection.record_dict
        coordinates = self.record_collection.coordinates
        timestamps = (self.record_collection.save_start_time,
                      self.record_collection.save_stop_time)

        # remove below if save each record in SaveRecordProcess()
        self.db_connector.insert_save_inform(coordinates, timestamps)

        record_count = [len(record_dict[_id]) for _id in record_dict.keys()]
        w_buffer = 'start_time: %s\nstop_time: %s' % timestamps
        w_buffer += '\nrecord_count: {}'.format(record_count)

        # for pmc
        if self.__is_pmc_construction(coordinates):
            if self.__is_enough_records(record_count):
                fp = dp.raw_to_fingerprint_pmc(record_dict)
                self.db_connector.insert_rm_point(coordinates, fp, record_count)
                w_buffer += '\nfp: ' + str(fp)
            else:
                w_buffer += "\nNot enough records"

        threading.Thread(target=self.reopen_server,
                         args=('save_stop_process',), daemon=True).start()

        self.record_collection.remove_records()
        self.send_msg_to_client(w_buffer)
