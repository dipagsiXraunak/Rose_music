from pyrogram.enums import ChatMemberStatus, ChatType
from config import OWNER_ID

async def is_owner(_, client, message):
    return message.from_user and message.from_user.id == OWNER_ID

async def is_admin(_, client, message):
    if message.chat.type == ChatType.PRIVATE: return True
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    return user.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)

async def safe_pin(message):
    try: await message.pin()
    except: pass
