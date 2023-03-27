import uuid
from Message import Message


class LoggingRepository:
    def __init__(self):
        self.logging = {}

    def get_all_messages(self):
        return list(self.logging.values())

    def log_message(self, msg: Message):
        u = msg.uuid
        if u in self.logging:
            u = uuid.uuid1()
        mes = msg.text
        print("Message: ", u, ":", mes)
        self.logging.update({u: mes})
