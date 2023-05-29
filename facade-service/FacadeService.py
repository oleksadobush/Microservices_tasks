import socket

import hazelcast
import requests
import random
import consul
from Message import Message
import os


class FacadeService:
    def __init__(self):
        self.client = hazelcast.HazelcastClient(cluster_members=["hazel1"])
        self.id = os.environ["S_ID"]
        self.service_name = 'facade'
        self.consul_service = consul.Consul(host="consul")
        self.q = self.client.get_queue(self.consul_service.kv.get('queue-name')[1]['Value'].decode('utf-8'))
        host = socket.gethostname()
        check = consul.Check.http(f"http://{host}:8080/health", "20s", "2s", "30s")
        self.consul_service.agent.service.register(self.service_name, service_id=self.service_name + self.id,
                                                   address=host, port=8080, check=check)

    def get_address(self, service_name):
        consul_info = self.consul_service.health.service(service_name)[1]
        address = random.choice(consul_info)["Service"]["Address"]
        port = random.choice(consul_info)["Service"]["Port"]
        return address, port

    def get_message(self):
        adr, p = self.get_address("logging")
        log_service = "http://" + str(adr) + ":" + str(p) + "/logging-service"
        print(log_service)
        response_log = requests.get(log_service).json()

        adr, p = self.get_address("messages")
        mes_service = "http://" + str(adr) + ":" + str(p) + "/messages-service"
        response_mes = requests.get(mes_service).text
        print("Logging Service: ", log_service, ".")
        print("Messaging Service: ", mes_service, ".")
        return ", ".join(response_log) + "\n" + response_mes

    def post_message(self, msg: Message):
        adr, p = self.get_address("logging")
        log_service = "http://" + str(adr) + ":" + str(p) + "/logging-service"
        print("Logging Service: ", log_service, ".")
        requests.post(log_service, data=msg.json())

        self.q.put(msg).result()

