import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, MONGO_URL
from utils.db import init_db

async def main():
    # Initialize database
    await init_db()
    
    # Create client
    app = Client(
        "RoseMusic",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        session_string=SESSION_STRING if SESSION_STRING else None
    )
    
    # /start command
    @app.on_message(filters.command("start"))
    async def start_command(client, message):
        await message.reply_text("🌸 Rose Music Bot is alive! Use /help for commands.")
    
    # Start the client
    await app.start()
    print("Bot started successfully!")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
