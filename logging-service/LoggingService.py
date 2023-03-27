from Message import Message
from LoggingHazRepository import LoggingRepository


class LoggingService:
    def __init__(self):
        self.repository = LoggingRepository()

    def get_message(self):
        return self.repository.get_all_messages()

    def post_message(self, msg: Message):
        print("Got the message: ", msg)
        return self.repository.log_message(msg)
