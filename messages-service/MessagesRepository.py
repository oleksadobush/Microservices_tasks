class MessagesRepository:
    def __init__(self):
        self.messages = []

    def add_message(self, mes):
        self.messages.append(mes)

    def get_messages(self):
        return self.messages
