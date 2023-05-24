import hazelcast
import requests
import random
from Message import Message


class FacadeService:
    def __init__(self):
        self.log_services = ["http://logging-service1:8080/logging-service",
                             "http://logging-service2:8080/logging-service",
                             "http://logging-service3:8080/logging-service"]
        self.message_services = ["http://messages-service1:8080/messages-service",
                                 "http://messages-service2:8080/messages-service"]
        client = hazelcast.HazelcastClient(cluster_members=["hazel1"])
        self.q = client.get_queue("mess-queue")

    def get_message(self):
        log_service = random.choice(self.log_services)
        response_log = requests.get(log_service).json()
        mes_service = random.choice(self.message_services)
        response_mes = requests.get(mes_service).text
        print("Logging Service: ", log_service, ".")
        print("Messaging Service: ", mes_service, ".")
        return ", ".join(response_log) + "\n" + response_mes

    def post_message(self, msg: Message):
        log_service = random.choice(self.log_services)
        print("Logging Service: ", log_service, ".")
        requests.post(log_service, data=msg.json())

        self.q.put(msg).result()
