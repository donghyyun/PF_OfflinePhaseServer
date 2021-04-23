import abc
import threading
import time
from datetime import datetime

from .AbstractProcess import AbstractProcess
from .SaveStopProcess import SaveStopProcess
from utils.threads import set_thread_name


class SaveStartProcess(AbstractProcess):
    @staticmethod
    def __parse_buffer(buffer):
        try:
            coordinates, collect_time = buffer.split('/')
            coordinates = tuple(int(i) for i in coordinates.split(','))
            collect_time = int(collect_time)
            return coordinates, collect_time

        except ValueError:
            coordinates = tuple(int(i) for i in buffer.split(','))
            return coordinates, None

    @staticmethod
    def __msg_to_send(coordinates):
        msg = ""
        try:
            from_x, from_y, to_x, to_y = coordinates
            msg += "'from' coordinate: (%d, %d)\n" % (from_x, from_y)
            msg += "'to' coordinate: (%d, %d)" % (to_x, to_y)
        except ValueError:
            x, y = coordinates
            msg += "Saving start-coordinate: (%d, %d)\n" % (x, y)
        finally:
            return msg

    @abc.abstractmethod
    def execute(self):
        set_thread_name("SAVE_START")
        print('\n>>>save_start_process', threading.current_thread())

        self.shutdown_and_wait()
        self.is_save = True

        buffer = self.request.recv(100).decode().strip()
        coordinate, collect_time = self.__parse_buffer(buffer)

        self.collection_details.coordinate = coordinate
        self.collection_details.save_start_time = datetime.now()

        threading.Thread(target=self.reopen_server,
                         args=('save_start_process',), daemon=True).start()

        msg = self.__msg_to_send(coordinate)
        self.send_msg_to_client(msg)

        if collect_time:
            set_thread_name("REOPEN")
            time.sleep(collect_time)
            SaveStopProcess(self.server, self.request).execute()
