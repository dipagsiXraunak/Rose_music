import asyncio, os
from threading import Thread
from flask import Flask
from pyrogram import Client
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, LOGGER_ID, MONGO_URI
from utils.logger import send_log
from utils.db import init_db

# Bot client
app = Client("ROSE_Music_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Assistant client
if not SESSION_STRING:
    raise ValueError("SESSION_STRING not set! Generate it using the helper script.")
user = Client("assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

call_py = PyTgCalls(user)

# Flask health
flask_app = Flask(__name__)
@flask_app.route('/')
def health():
    return "ROSE Bot is running", 200

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    flask_app.run(host='0.0.0.0', port=port)

# Heartbeat
async def heartbeat():
    while True:
        await asyncio.sleep(300)
        if LOGGER_ID:
            await send_log(app, "✅ ROSE Music Bot is alive and running!")

async def main():
    # Init MongoDB
    await init_db(MONGO_URI)

    await app.start()
    await user.start()
    await call_py.start()
    asyncio.create_task(heartbeat())
    await send_log(app, "🤖 ROSE Music Bot started successfully!")
    print("🤖 ROSE Music Bot (Assistant Mode) with MongoDB is alive...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
