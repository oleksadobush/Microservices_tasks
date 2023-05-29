import socket
from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI

from MessagesRepository import MessagesRepository
import hazelcast
import os
import consul


class MessagesService:
    def __init__(self):
        self.client = hazelcast.HazelcastClient(cluster_members=["hazel1"])
        self.consul_service = consul.Consul(host="consul")
        self.q = self.client.get_queue(self.consul_service.kv.get('queue-name')[1]['Value'].decode('utf-8'))

        self.repository = MessagesRepository()
        self.loop = asyncio.get_running_loop()
        self.id = os.environ["S_ID"]
        self.service_name = 'messages'
        self.consul_service = consul.Consul(host="consul")
        host = socket.gethostname()
        check = consul.Check.http(f"http://{host}:8080/health", "20s", "2s", "30s")
        self.consul_service.agent.service.register(self.service_name, service_id=self.service_name + self.id,
                                                   address=host, port=8080, check=check)

    def get_messages(self):
        return self.repository.get_messages()
    
    async def process_messages(self):
        while True:
            if self.q.is_empty().result():
                await asyncio.sleep(0.1)
            else:
                mes = self.q.take().result()
                mes = mes.text
                print('Message: ', mes)
                self.repository.add_message(mes)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        self.loop.create_task(self.process_messages())
        yield
