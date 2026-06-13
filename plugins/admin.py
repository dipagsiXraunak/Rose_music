from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from main import app
from utils.helpers import is_admin
from utils.logger import send_log
from config import OWNER_ID

@app.on_message(filters.command(["ban","mute"]) & filters.group)
@filters.create(is_admin)
async def ban_mute(client, message):
    cmd = message.command[0]
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try: user = await client.get_users(message.command[1])
        except: return await message.reply("❌ User not found.")
    else: return await message.reply("Reply or give username/id.")
    if user.id == (await client.get_me()).id: return await message.reply("❌ Can't restrict myself.")
    if user.id == OWNER_ID: return await message.reply("❌ Owner ko restrict nahi kar sakta.")
    if cmd == "ban":
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply(f"🚫 {user.first_name} banned.")
        await send_log(client, f"🚫 /ban by {message.from_user.mention} on {user.mention} in {message.chat.title} [{message.chat.id}]")
    else:
        await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=False))
        await message.reply(f"🔇 {user.first_name} muted.")
        await send_log(client, f"🔇 /mute by {message.from_user.mention} on {user.mention} in {message.chat.title} [{message.chat.id}]")

@app.on_message(filters.command("unban") & filters.group)
@filters.create(is_admin)
async def unban(client, message):
    if message.reply_to_message: user = message.reply_to_message.from_user
    elif len(message.command)>1:
        try: user = await client.get_users(message.command[1])
        except: return await message.reply("User not found.")
    else: return await message.reply("Reply or give username/id.")
    await client.unban_chat_member(message.chat.id, user.id)
    await message.reply(f"✅ {user.first_name} unbanned.")
    await send_log(client, f"✅ /unban by {message.from_user.mention} on {user.mention} in {message.chat.title} [{message.chat.id}]")

@app.on_message(filters.command("unmute") & filters.group)
@filters.create(is_admin)
async def unmute(client, message):
    if message.reply_to_message: user = message.reply_to_message.from_user
    elif len(message.command)>1:
        try: user = await client.get_users(message.command[1])
        except: return await message.reply("User not found.")
    else: return await message.reply("Reply or give username/id.")
    await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=True))
    await message.reply(f"🔊 {user.first_name} unmuted.")
    await send_log(client, f"🔊 /unmute by {message.from_user.mention} on {user.mention} in {message.chat.title} [{message.chat.id}]")
