from pydantic import BaseModel
import uuid


class Message(BaseModel):
    text: str
    uuid = uuid.uuid1()

