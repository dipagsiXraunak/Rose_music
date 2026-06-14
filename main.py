import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, MONGO_URL
from utils.db import init_db

async def main():
    # Check MongoDB URI
    if not MONGO_URL or MONGO_URL.startswith("your_"):
        print("❌ ERROR: MONGO_URL is not set in environment variables.")
        return
    
    # Initialize database connection
    try:
        await init_db()
        print("✅ Database ready")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Create client
    app = Client(
        "RoseMusic",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        session_string=SESSION_STRING if SESSION_STRING else None,
        in_memory=True
    )
    
    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):
        await message.reply_text("🌸 Rose Music Bot is alive! Use /help for commands.")
    
    @app.on_message(filters.command("ping"))
    async def ping_cmd(client, message):
        await message.reply_text("🏓 Pong!")
    
    print("🚀 Starting bot...")
    await app.start()
    print("✅ Bot is running! Press Ctrl+C to stop.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
