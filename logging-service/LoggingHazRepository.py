import uuid

import consul
import hazelcast

from Message import Message


class LoggingRepository:
    def __init__(self):
        self.client = hazelcast.HazelcastClient(cluster_members=["hazel1"])
        self.consul_service = consul.Consul(host="consul")
        self.logging = self.client.get_map(
            self.consul_service.kv.get('map-name')[1]['Value'].decode('utf-8')).blocking()

    def get_all_messages(self):
        return list(self.logging.values())

    def log_message(self, msg: Message):
        u = msg.uuid
        if self.logging.contains_key(u):
            u = uuid.uuid1()
        mes = msg.text
        self.logging.lock(u)
        print("Message: ", u, ":", mes)
        self.logging.put(u, mes)
        self.logging.unlock(u)
