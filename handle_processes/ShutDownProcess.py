import abc
import threading

from .AbstractProcess import AbstractProcess


class ShutDownProcess(AbstractProcess):
    @abc.abstractmethod
    def execute(self):
        self.set_thread_name("SHUTDOWN")
        print('\n>>>shutdown process::', threading.current_thread())

        self.shutdown_and_wait()
        self.db_connector.close()

        # Just for debugging
        print('-Active threads(In shutdown process)-\n', threading.enumerate())
