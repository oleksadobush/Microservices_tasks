import socket
from Message import Message
from LoggingHazRepository import LoggingRepository
import os
import consul


class LoggingService:
    def __init__(self):
        self.repository = LoggingRepository()
        self.id = os.environ["S_ID"]
        self.service_name = 'logging'
        self.consul_service = consul.Consul(host="consul")
        host = socket.gethostname()
        check = consul.Check.http(f"http://{host}:8080/health", "20s", "2s", "30s")
        self.consul_service.agent.service.register(self.service_name, service_id=self.service_name + self.id,
                                                   address=host, port=8080, check=check)

    def get_message(self):
        return self.repository.get_all_messages()

    def post_message(self, msg: Message):
        print("Got the message: ", msg)
        return self.repository.log_message(msg)
