import requests
import random
from Message import Message


class FacadeService:
    def __init__(self):
        self.services = ["http://logging-service1:8080/logging-service",
                         "http://logging-service2:8080/logging-service",
                         "http://logging-service3:8080/logging-service"]
        self.message_service = "http://messages-service:8080/messages-service"

    def get_message(self):
        service = random.choice(self.services)
        response_log = requests.get(service).json()
        response_mes = requests.get(self.message_service).text
        print("Logging Service: ", service, ".")
        return ", ".join(response_log) + "\n" + response_mes[1:-1]

    def post_message(self, msg: Message):
        service = random.choice(self.services)
        print("Logging Service: ", service, ".")
        requests.post(service, data=msg.json())
