from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pyrogram import Client
from .queue import QueueManager

class MusicPlayer:
    def __init__(self):
        self.active_chats = {}
        self.queue = QueueManager()

    async def play_audio(self, client, call_py, chat_id, audio_url, title):
        try:
            await call_py.join_group_call(chat_id, AudioPiped(audio_url), stream_type=StreamType().pulse_stream)
            self.active_chats[chat_id] = {'title': title, 'status': 'playing', 'type': 'audio'}
        except Exception as e:
            print(f"Audio play error: {e}")

    async def play_video(self, client, call_py, chat_id, video_url, title):
        try:
            await call_py.join_group_call(chat_id, AudioVideoPiped(video_url), stream_type=StreamType().pulse_stream)
            self.active_chats[chat_id] = {'title': title, 'status': 'playing', 'type': 'video'}
        except Exception as e:
            print(f"Video play error: {e}")

    async def play_or_enqueue(self, client, call_py, chat_id, url, title, stream_type):
        if chat_id in self.active_chats and self.active_chats[chat_id]['status'] == 'playing':
            self.queue.add(chat_id, url, title, stream_type)
            return "queued"
        else:
            if stream_type == 'audio':
                await self.play_audio(client, call_py, chat_id, url, title)
            else:
                await self.play_video(client, call_py, chat_id, url, title)
            return "playing"

    async def play_next(self, client, call_py, chat_id):
        next_item = self.queue.get_next(chat_id)
        if next_item:
            url, title, stream_type = next_item
            if stream_type == 'audio':
                await self.play_audio(client, call_py, chat_id, url, title)
            else:
                await self.play_video(client, call_py, chat_id, url, title)
            return title
        return None

    async def stop(self, call_py, chat_id):
        await call_py.leave_group_call(chat_id)
        self.active_chats.pop(chat_id, None)
        self.queue.clear(chat_id)

player = MusicPlayer()
