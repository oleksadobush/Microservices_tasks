from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI

from MessagesRepository import MessagesRepository
import hazelcast


class MessagesService:
    def __init__(self):
        client = hazelcast.HazelcastClient(cluster_members=["hazel1"])
        self.q = client.get_queue("mess-queue")
        self.repository = MessagesRepository()
        self.loop = asyncio.get_running_loop()

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
