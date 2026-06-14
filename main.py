from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING
from utils.db import init_db

# Initialize database
init_db()

app = Client(
    "RoseMusic",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    session_string=SESSION_STRING if SESSION_STRING else None
)

if __name__ == "__main__":
    print("🌸 Rose Music Bot Started!")
    app.run()
