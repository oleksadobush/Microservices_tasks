from fastapi import FastAPI
from LoggingService import LoggingService
from Message import Message


class LoggingController:

    def __init__(self):
        self.app = FastAPI()
        self.service = LoggingService()

        @self.app.get('/logging-service')
        def get_message():
            return self.service.get_message()

        @self.app.post('/logging-service')
        def post_message(msg: Message):
            return self.service.post_message(msg)


log = LoggingController()
