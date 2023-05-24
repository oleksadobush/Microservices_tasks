from fastapi import FastAPI
from MessagesService import MessagesService


class MessagesController:
    def __init__(self):
        self.service = MessagesService()
        self.app = FastAPI(lifespan=self.service.lifespan)

        @self.app.get('/messages-service')
        def get_messages():
            return self.service.get_messages()


mes = MessagesController()
