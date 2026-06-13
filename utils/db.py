from motor.motor_asyncio import AsyncIOMotorClient

# Global collections
db = None
groups_col = None
users_col = None

async def init_db(uri: str):
    global db, groups_col, users_col
    client = AsyncIOMotorClient(uri)
    db = client.rose_music_bot
    groups_col = db.groups   # stores group IDs
    users_col = db.users     # stores user IDs
    print("✅ MongoDB connected!")

# --- Group persistence ---
async def save_group(chat_id: int):
    await groups_col.update_one({"_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)

async def load_groups() -> set:
    groups = set()
    async for doc in groups_col.find({}):
        groups.add(doc["chat_id"])
    return groups

# --- User persistence ---
async def save_user(user_id: int):
    await users_col.update_one({"_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

async def load_users() -> set:
    users = set()
    async for doc in users_col.find({}):
        users.add(doc["user_id"])
    return users
