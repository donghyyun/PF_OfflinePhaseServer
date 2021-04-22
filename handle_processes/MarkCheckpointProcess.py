import abc

from .AbstractProcess import AbstractProcess
from utils.threads import set_thread_name


class MarkCheckpointProcess(AbstractProcess):
    @abc.abstractmethod
    def execute(self):
        set_thread_name('Mark_Checkpoint')

        if not self.is_save:
            self.send_msg_to_client('Please press saving start button.\n'
                                    'No data is currently being collected.')
            return

        self.db_connector.insert_checkpoint()
        self.send_msg_to_client('checkpoint is recorded')
