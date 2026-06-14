from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from main import app, user, call_py
from config import OWNER_ID, THUMBNAIL_URL
from utils.yt_utils import get_audio_url, get_video_url
from music.player import player
from utils.logger import send_log

async def ensure_voice_chat(client, chat_id):
    try: await client.get_group_call(chat_id)
    except: await client.create_group_call(chat_id)

# Music
@app.on_message(filters.command("play") & filters.group & filters.user(OWNER_ID))
async def owner_play(client, message):
    if len(message.command) < 2: return await message.reply("❌ Usage: /play <song>")
    query = message.text.split(maxsplit=1)[1]
    msg = await message.reply(f"🔍 Searching `{query}`...")
    url, title = get_audio_url(query)
    if not url: return await msg.edit("❌ Not found.")
    await ensure_voice_chat(user, message.chat.id)
    status = await player.play_or_enqueue(user, call_py, message.chat.id, url, title, 'audio')
    if status == "playing":
        if THUMBNAIL_URL:
            try: await msg.delete(); await msg.chat.send_photo(THUMBNAIL_URL, caption=f"🎵 Now playing: **{title}** ❤️‍🔥")
            except: await msg.edit(f"🎵 Now playing: **{title}** ❤️‍🔥")
        else: await msg.edit(f"🎵 Now playing: **{title}** ❤️‍🔥")
    else: await msg.edit(f"🎵 Added to queue: **{title}**")
    await send_log(client, f"👑 Owner /play: {title} in {message.chat.title}")

@app.on_message(filters.command("vplay") & filters.group & filters.user(OWNER_ID))
async def owner_vplay(client, message):
    if len(message.command) < 2: return await message.reply("❌ Usage: /vplay <video>")
    query = message.text.split(maxsplit=1)[1]
    msg = await message.reply(f"🔍 Searching `{query}`...")
    url, title = get_video_url(query)
    if not url: return await msg.edit("❌ Not found.")
    await ensure_voice_chat(user, message.chat.id)
    status = await player.play_or_enqueue(user, call_py, message.chat.id, url, title, 'video')
    if status == "playing":
        if THUMBNAIL_URL:
            try: await msg.delete(); await msg.chat.send_photo(THUMBNAIL_URL, caption=f"📹 Now streaming: **{title}**")
            except: await msg.edit(f"📹 Now streaming: **{title}**")
        else: await msg.edit(f"📹 Now streaming: **{title}**")
    else: await msg.edit(f"📹 Added to queue: **{title}**")
    await send_log(client, f"👑 Owner /vplay: {title} in {message.chat.title}")

@app.on_message(filters.command("skip") & filters.group & filters.user(OWNER_ID))
async def owner_skip(client, message):
    chat_id = message.chat.id
    if chat_id in player.active_chats:
        await player.stop(call_py, chat_id)
        await message.reply("⏭ Skipped by Owner.")
        await send_log(client, f"👑 Owner /skip in {message.chat.title}")
    else: await message.reply("❌ Nothing playing.")

@app.on_message(filters.command("end") & filters.group & filters.user(OWNER_ID))
async def owner_end(client, message):
    chat_id = message.chat.id
    if chat_id in player.active_chats:
        await player.stop(call_py, chat_id)
        await message.reply("⏹ Ended by Owner.\n🔇 **ROSE** ne voice chat chhod di. 🍬")
        await send_log(client, f"👑 Owner /end in {message.chat.title}")
    else: await message.reply("❌ Not in voice chat.")

@app.on_message(filters.command("pause") & filters.group & filters.user(OWNER_ID))
async def owner_pause(client, message):
    chat_id = message.chat.id
    if chat_id in player.active_chats and player.active_chats[chat_id]['status'] == 'playing':
        await call_py.pause_stream(chat_id)
        player.active_chats[chat_id]['status'] = 'paused'
        await message.reply("⏸ Paused by Owner.")
        await send_log(client, f"👑 Owner /pause in {message.chat.title}")
    else: await message.reply("❌ Nothing playing.")

@app.on_message(filters.command("resume") & filters.group & filters.user(OWNER_ID))
async def owner_resume(client, message):
    chat_id = message.chat.id
    if chat_id in player.active_chats and player.active_chats[chat_id]['status'] == 'paused':
        await call_py.resume_stream(chat_id)
        player.active_chats[chat_id]['status'] = 'playing'
        await message.reply("▶ Resumed by Owner.")
        await send_log(client, f"👑 Owner /resume in {message.chat.title}")
    else: await message.reply("❌ Not paused.")

@app.on_message(filters.command("stop") & filters.group & filters.user(OWNER_ID))
async def owner_stop(client, message):
    chat_id = message.chat.id
    if chat_id in player.active_chats:
        await player.stop(call_py, chat_id)
        await message.reply("⏹ Stopped by Owner.")
        await send_log(client, f"👑 Owner /stop in {message.chat.title}")
    else: await message.reply("❌ Not in voice chat.")

# Ban/Mute
@app.on_message(filters.command(["ban","mute"]) & filters.group & filters.user(OWNER_ID))
async def owner_ban_mute(client, message):
    cmd = message.command[0]
    if message.reply_to_message: user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try: user = await client.get_users(message.command[1])
        except: return await message.reply("❌ User not found.")
    else: return await message.reply("Reply or give username/id.")
    if user.id == (await client.get_me()).id: return await message.reply("❌ Can't restrict myself.")
    if cmd == "ban":
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply(f"🚫 {user.first_name} banned by Owner.")
        await send_log(client, f"👑 Owner /ban on {user.mention}")
    else:
        await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=False))
        await message.reply(f"🔇 {user.first_name} muted by Owner.")
        await send_log(client, f"👑 Owner /mute on {user.mention}")

@app.on_message(filters.command("unban") & filters.group & filters.user(OWNER_ID))
async def owner_unban(client, message):
    if message.reply_to_message: user = message.reply_to_message.from_user
    elif len(message.command)>1:
        try: user = await client.get_users(message.command[1])
        except: return await message.reply("User not found.")
    else: return await message.reply("Reply or give username/id.")
    await client.unban_chat_member(message.chat.id, user.id)
    await message.reply(f"✅ {user.first_name} unbanned by Owner.")
    await send_log(client, f"👑 Owner /unban on {user.mention}")

@app.on_message(filters.command("unmute") & filters.group & filters.user(OWNER_ID))
async def owner_unmute(client, message):
    if message.reply_to_message: user = message.reply_to_message.from_user
    elif len(message.command)>1:
        try: user = await client.get_users(message.command[1])
        except: return await message.reply("User not found.")
    else: return await message.reply("Reply or give username/id.")
    await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=True))
    await message.reply(f"🔊 {user.first_name} unmuted by Owner.")
    await send_log(client, f"👑 Owner /unmute on {user.mention}")

# Gban/Gunban
async def get_all_groups():
    from plugins.owner import joined_groups
    return joined_groups

@app.on_message(filters.command("gban") & filters.user(OWNER_ID))
async def gban_cmd(client, message):
    if len(message.command) < 2: return await message.reply("Usage: /gban <user_id/username>")
    try: user_to_ban = await client.get_users(message.command[1])
    except: return await message.reply("❌ User not found.")
    groups = await get_all_groups()
    count = 0
    for chat_id in groups:
        try: await client.ban_chat_member(chat_id, user_to_ban.id); count += 1
        except: pass
    await message.reply(f"🚫 {user_to_ban.mention} globally banned from {count} groups.")
    await send_log(client, f"👑 /gban on {user_to_ban.mention} - {count} groups")

@app.on_message(filters.command("gunban") & filters.user(OWNER_ID))
async def gunban_cmd(client, message):
    if len(message.command) < 2: return await message.reply("Usage: /gunban <user_id/username>")
    try: user_to_unban = await client.get_users(message.command[1])
    except: return await message.reply("❌ User not found.")
    groups = await get_all_groups()
    count = 0
    for chat_id in groups:
        try: await client.unban_chat_member(chat_id, user_to_unban.id); count += 1
        except: pass
    await message.reply(f"✅ {user_to_unban.mention} globally unbanned from {count} groups.")
    await send_log(client, f"👑 /gunban on {user_to_unban.mention} - {count} groups")

# Banall
@app.on_message(filters.command("banall") & filters.group & filters.user(OWNER_ID))
async def banall_cmd(client, message):
    chat_id = message.chat.id
    bot_member = await client.get_chat_member(chat_id, "me")
    if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
        return await message.reply("❌ Bot ko ban permission nahi hai.")
    await message.reply("🚫 Banning all non-admin members...")
    count = 0
    async for member in client.get_chat_members(chat_id):
        if member.user.id == app.me.id: continue
        if member.status in ("administrator", "creator"): continue
        try: await client.ban_chat_member(chat_id, member.user.id); count += 1
        except: pass
    await message.reply(f"✅ Banned {count} members. Only admins left.")
    await send_log(client, f"👑 Owner /banall in {message.chat.title} - {count} banned")
