from .AbstractProcess import AbstractProcess


class MarkCheckpointProcess(AbstractProcess):
    def execute(self):
        if not self.is_save:
            self.send_msg_to_client('Please press saving start button.\n'
                                    'No data is currently being collected.')
            return

        self.db_connector.insert_checkpoint()
        self.send_msg_to_client('checkpoint is recorded')
