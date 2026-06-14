from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from main import app, user, call_py
from music.player import player
from utils.helpers import is_admin
from utils.logger import send_log
from utils.yt_utils import get_audio_url, get_video_url
from config import THUMBNAIL_URL, OWNER_ID

async def ensure_voice_chat(client, chat_id):
    try: await client.get_group_call(chat_id)
    except: await client.create_group_call(chat_id)

@app.on_message(filters.command("play") & filters.group & ~filters.user(OWNER_ID))
@filters.create(is_admin)
async def admin_play(client, message):
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
    await send_log(client, f"🛡 Admin /play: {title} by {message.from_user.mention}")

@app.on_message(filters.command("vplay") & filters.group & ~filters.user(OWNER_ID))
@filters.create(is_admin)
async def admin_vplay(client, message):
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
    await send_log(client, f"🛡 Admin /vplay: {title} by {message.from_user.mention}")

@app.on_message(filters.command("skip") & filters.group)
@filters.create(is_admin)
async def admin_skip(client, message):
    chat_id = message.chat.id
    if chat_id in player.active_chats:
        await player.stop(call_py, chat_id)
        await message.reply("⏭ Skipped by Admin.")
        await send_log(client, f"🛡 /skip by {message.from_user.mention}")
    else: await message.reply("❌ Nothing playing.")

@app.on_message(filters.command("end") & filters.group)
@filters.create(is_admin)
async def admin_end(client, message):
    chat_id = message.chat.id
    if chat_id in player.active_chats:
        await player.stop(call_py, chat_id)
        await message.reply("⏹ Ended by Admin.\n🔇 **ROSE** ne voice chat chhod di. 🍬")
        await send_log(client, f"🛡 /end by {message.from_user.mention}")
    else: await message.reply("❌ Not in voice chat.")

@app.on_message(filters.command("pause") & filters.group)
@filters.create(is_admin)
async def pause_cmd(client, message):
    chat_id = message.chat.id
    if chat_id in player.active_chats and player.active_chats[chat_id]['status'] == 'playing':
        await call_py.pause_stream(chat_id)
        player.active_chats[chat_id]['status'] = 'paused'
        await message.reply("⏸ Paused.")
        await send_log(client, f"🛡 Pause by {message.from_user.mention}")
    else: await message.reply("❌ Nothing playing.")

@app.on_message(filters.command("resume") & filters.group)
@filters.create(is_admin)
async def resume_cmd(client, message):
    chat_id = message.chat.id
    if chat_id in player.active_chats and player.active_chats[chat_id]['status'] == 'paused':
        await call_py.resume_stream(chat_id)
        player.active_chats[chat_id]['status'] = 'playing'
        await message.reply("▶ Resumed.")
        await send_log(client, f"🛡 Resume by {message.from_user.mention}")
    else: await message.reply("❌ Not paused.")

@app.on_message(filters.command("stop") & filters.group)
@filters.create(is_admin)
async def stop_cmd(client, message):
    chat_id = message.chat.id
    if chat_id in player.active_chats:
        await player.stop(call_py, chat_id)
        await message.reply("⏹ Stopped.")
        await send_log(client, f"🛡 Stop by {message.from_user.mention}")
    else: await message.reply("❌ Not in voice chat.")

@app.on_message(filters.command(["ban","mute"]) & filters.group)
@filters.create(is_admin)
async def ban_mute(client, message):
    cmd = message.command[0]
    if message.reply_to_message: user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try: user = await client.get_users(message.command[1])
        except: return await message.reply("❌ User not found.")
    else: return await message.reply("Reply or give username/id.")
    if user.id == (await client.get_me()).id: return await message.reply("❌ Can't restrict myself.")
    if user.id == OWNER_ID: return await message.reply("❌ Owner ko restrict nahi kar sakta.")
    if cmd == "ban":
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply(f"🚫 {user.first_name} banned.")
        await send_log(client, f"🚫 /ban by {message.from_user.mention} on {user.mention}")
    else:
        await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=False))
        await message.reply(f"🔇 {user.first_name} muted.")
        await send_log(client, f"🔇 /mute by {message.from_user.mention} on {user.mention}")

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
    await send_log(client, f"✅ /unban by {message.from_user.mention}")

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
    await send_log(client, f"🔊 /unmute by {message.from_user.mention}")
