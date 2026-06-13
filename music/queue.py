from collections import deque

class QueueManager:
    def __init__(self):
        self.queues = {}

    def add(self, chat_id, url, title, stream_type):
        if chat_id not in self.queues:
            self.queues[chat_id] = deque()
        self.queues[chat_id].append((url, title, stream_type))

    def get_next(self, chat_id):
        if chat_id in self.queues and self.queues[chat_id]:
            return self.queues[chat_id].popleft()
        return None

    def clear(self, chat_id):
        if chat_id in self.queues:
            self.queues[chat_id].clear()

    def get_queue_text(self, chat_id):
        if chat_id not in self.queues or not self.queues[chat_id]:
            return "Queue is empty."
        items = [f"{i+1}. {title}" for i, (_, title, _) in enumerate(self.queues[chat_id])]
        return "📋 **Queue:**\n" + "\n".join(items)
