from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import app
from config import OWNER_ID, SUPPORT_LINK, UPDATE_LINK, OWNER_LINK, SOURCE_LINK, WELCOME_IMAGE_URL
from utils.helpers import safe_pin
from utils.logger import send_log
from utils.db import save_group, save_user, load_groups, load_users

joined_groups = set()
joined_users = set()

async def init_persistence():
    global joined_groups, joined_users
    joined_groups = await load_groups()
    joined_users = await load_users()
    print(f"Loaded {len(joined_groups)} groups and {len(joined_users)} users from DB.")

KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("📣 Support", url=SUPPORT_LINK),
     InlineKeyboardButton("🔔 Updates", url=UPDATE_LINK)],
    [InlineKeyboardButton("👑 Owner", url=OWNER_LINK),
     InlineKeyboardButton("📂 Source Code", url=SOURCE_LINK)],
    [InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{app.me.username}?startgroup=true")]
])

@app.on_message(filters.command("start"))
async def pm_start(client, message):
    joined_users.add(message.from_user.id)
    await save_user(message.from_user.id)
    caption = (
        f"🌸 **{app.me.first_name}** ❤️‍🔥\n\n"
        "👋 Hello! Main **ROSE Music Bot** hoon.\n"
        "Apne group mein add karo aur music ka maza lo!\n\n"
        "Commands: /help"
    )
    if WELCOME_IMAGE_URL:
        try:
            await message.reply_photo(WELCOME_IMAGE_URL, caption=caption, reply_markup=KEYBOARD)
        except:
            await message.reply(caption, reply_markup=KEYBOARD)
    else:
        await message.reply(caption, reply_markup=KEYBOARD)
    await send_log(client, f"👋 /start by {message.from_user.mention} [{message.from_user.id}]")

@app.on_chat_member_updated()
async def track_groups(client, event):
    if event.new_chat_member and event.new_chat_member.user.id == (await client.get_me()).id:
        joined_groups.add(event.chat.id)
        await save_group(event.chat.id)
        await send_log(client, f"➕ Bot added to group: {event.chat.title} [{event.chat.id}]")

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_groups(client, message):
    if len(message.command) < 2: return await message.reply("Give a message.")
    text = message.text.split(maxsplit=1)[1]
    count = 0
    for chat_id in joined_groups.copy():
        try:
            sent = await client.send_message(chat_id, text)
            await safe_pin(sent)
            count += 1
        except: pass
    await message.reply(f"✅ Broadcast to {count} groups.")
    await send_log(client, f"📢 Broadcast by owner to {count} groups.")

@app.on_message(filters.command("pmcast") & filters.user(OWNER_ID))
async def broadcast_users(client, message):
    if len(message.command) < 2: return await message.reply("Give a message.")
    text = message.text.split(maxsplit=1)[1]
    count = 0
    for user_id in joined_users.copy():
        try:
            await client.send_message(user_id, text)
            count += 1
        except: pass
    await message.reply(f"✅ PM broadcast to {count} users.")
    await send_log(client, f"📬 PM broadcast by owner to {count} users.")

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    await message.reply(f"👥 Groups: {len(joined_groups)}\n👤 Users: {len(joined_users)}")
    await send_log(client, f"📊 /stats by owner")
