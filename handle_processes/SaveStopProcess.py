import abc
import threading
import time
from datetime import datetime

from setting import PMC_MIN_FP
from .AbstractProcess import AbstractProcess
from utils.threads import set_thread_name


class SaveStopProcess(AbstractProcess):
    @staticmethod
    def __is_enough_records(record_count):
        if min(record_count) < PMC_MIN_FP:
            return False
        return True

    @staticmethod
    def __is_pmc_construction(coordinates):
        try:
            _, _, _, _ = coordinates
            return False
        except ValueError:
            return True

    @abc.abstractmethod
    def execute(self):
        set_thread_name("SAVE_STOP")
        print('\n>>>save_stop_process', threading.current_thread())

        self.collection_details.save_stop_time = datetime.now()
        time.sleep(1)

        self.shutdown_and_wait()
        self.is_save = False

        self.db_connector.insert_collection_details(self.collection_details)

        w_buffer = f'start_time: {self.collection_details.save_start_time}\n' \
                   f'stop_time: {self.collection_details.save_stop_time}' \
                   f'record_count: {self.collection_details.record_count()}'

        # for pmc
        if self.__is_pmc_construction(self.collection_details.coordinate):
            if self.__is_enough_records(self.collection_details.record_count()):
                # need to implement for pmc rm construction
                w_buffer += '\nenough records for PMC'
            else:
                w_buffer += "\nNot enough records"

        threading.Thread(target=self.reopen_server,
                         args=('save_stop_process',), daemon=True).start()

        self.collection_details.clear()
        self.send_msg_to_client(w_buffer)
