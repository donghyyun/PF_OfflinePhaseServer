import abc
import threading
import time

from .AbstractProcess import AbstractProcess
from .SaveStopProcess import SaveStopProcess


class SaveStartProcess(AbstractProcess):
    ########################################
    # TO-DO: 좌표, 수집기간 외에 다른 정보(ex. location name)
    #       들어왔을때 split
    ########################################
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
        self.set_thread_name("SAVE_START")
        print('\n>>>save_start_process', threading.current_thread())

        self.shutdown_and_wait()
        self.is_save = True

        buffer = self.request.recv(100).decode().strip()
        coordinates, collect_time = self.__parse_buffer(buffer)

        self.record_collection.set_coordinates(coordinates)
        self.record_collection.set_start_time()

        threading.Thread(target=self.reopen_server,
                         args=('save_start_process',), daemon=True).start()

        msg = self.__msg_to_send(coordinates)
        self.send_msg_to_client(msg)

        if collect_time:
            time.sleep(collect_time)
            SaveStopProcess(self.server, self.request).execute()
