from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from FacadeService import FacadeService
from Message import Message


class FacadeController:

    def __init__(self):
        self.service = FacadeService()
        self.app = FastAPI()

        @self.app.get("/facade-service", response_class=PlainTextResponse)
        def get_message():
            return self.service.get_message()

        @self.app.post("/facade-service")
        def post_message(msg: Message):
            return self.service.post_message(msg)


fac = FacadeController()
