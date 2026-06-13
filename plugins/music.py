from pyrogram import Client, filters
from main import app, user, call_py
from utils.yt_utils import get_audio_url, get_video_url
from music.player import player
from utils.helpers import is_admin
from utils.logger import send_log
from config import THUMBNAIL_URL

async def ensure_voice_chat(client, chat_id):
    try:
        await client.get_group_call(chat_id)
    except:
        await client.create_group_call(chat_id)

async def send_play_message(msg, title, stream_type="audio"):
    icon = "🎵" if stream_type == "audio" else "📹"
    caption = f"{icon} Now playing: **{title}** ❤️‍🔥"
    if THUMBNAIL_URL:
        try:
            await msg.delete()
            await msg.chat.send_photo(THUMBNAIL_URL, caption=caption)
        except:
            await msg.edit(caption)
    else:
        await msg.edit(caption)

async def send_queue_message(msg, title, stream_type="audio"):
    icon = "🎵" if stream_type == "audio" else "📹"
    await msg.edit(f"{icon} Added to queue: **{title}**")

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(client, message):
    if len(message.command) < 2: return await message.reply("❌ Usage: /play <song>")
    query = message.text.split(maxsplit=1)[1]
    msg = await message.reply(f"🔍 Searching `{query}`...")
    url, title = get_audio_url(query)
    if not url: return await msg.edit("❌ Not found.")
    await ensure_voice_chat(user, message.chat.id)
    status = await player.play_or_enqueue(user, call_py, message.chat.id, url, title, 'audio')
    if status == "playing":
        await send_play_message(msg, title, 'audio')
    else:
        await send_queue_message(msg, title, 'audio')
    await send_log(client, f"🎵 /play by {message.from_user.mention} in {message.chat.title} [{message.chat.id}]\nQuery: {query}\nStatus: {status}")

@app.on_message(filters.command("vplay") & filters.group)
async def vplay_cmd(client, message):
    if len(message.command) < 2: return await message.reply("❌ Usage: /vplay <video>")
    query = message.text.split(maxsplit=1)[1]
    msg = await message.reply(f"🔍 Searching `{query}`...")
    url, title = get_video_url(query)
    if not url: return await msg.edit("❌ Not found.")
    await ensure_voice_chat(user, message.chat.id)
    status = await player.play_or_enqueue(user, call_py, message.chat.id, url, title, 'video')
    if status == "playing":
        await send_play_message(msg, title, 'video')
    else:
        await send_queue_message(msg, title, 'video')
    await send_log(client, f"📹 /vplay by {message.from_user.mention} in {message.chat.title} [{message.chat.id}]\nQuery: {query}")

@app.on_message(filters.command("anonplay") & filters.group)
async def anonplay_cmd(client, message):
    if len(message.command) < 2: return await message.reply("❌ Usage: /anonplay <song>")
    try: await message.delete()
    except: pass
    query = message.text.split(maxsplit=1)[1]
    url, title = get_audio_url(query)
    if not url: return await client.send_message(message.chat.id, "❌ Not found.")
    await ensure_voice_chat(user, message.chat.id)
    status = await player.play_or_enqueue(user, call_py, message.chat.id, url, title, 'audio')
    if status == "playing":
        if THUMBNAIL_URL:
            await client.send_photo(message.chat.id, THUMBNAIL_URL, caption=f"🎵 Now playing: **{title}**")
        else:
            await client.send_message(message.chat.id, f"🎵 Now playing: **{title}**")
    else:
        await client.send_message(message.chat.id, f"🎵 Added to queue: **{title}**")
    await send_log(client, f"🕶 /anonplay by {message.from_user.mention} in {message.chat.title} [{message.chat.id}]\nQuery: {query}")

@app.on_message(filters.command("queue") & filters.group)
async def queue_cmd(client, message):
    await message.reply(player.queue.get_queue_text(message.chat.id))
    await send_log(client, f"📋 /queue by {message.from_user.mention} in {message.chat.title} [{message.chat.id}]")

@app.on_message(filters.command("pause") & filters.group)
@filters.create(is_admin)
async def pause_cmd(client, message):
    if message.chat.id in player.active_chats and player.active_chats[message.chat.id]['status'] == 'playing':
        await call_py.pause_stream(message.chat.id)
        player.active_chats[message.chat.id]['status'] = 'paused'
        await message.reply("⏸ Paused.")
        await send_log(client, f"⏸ Pause by {message.from_user.mention} in {message.chat.title} [{message.chat.id}]")
    else:
        await message.reply("❌ Nothing playing.")

@app.on_message(filters.command("resume") & filters.group)
@filters.create(is_admin)
async def resume_cmd(client, message):
    if message.chat.id in player.active_chats and player.active_chats[message.chat.id]['status'] == 'paused':
        await call_py.resume_stream(message.chat.id)
        player.active_chats[message.chat.id]['status'] = 'playing'
        await message.reply("▶ Resumed.")
        await send_log(client, f"▶ Resume by {message.from_user.mention} in {message.chat.title} [{message.chat.id}]")
    else:
        await message.reply("❌ Not paused.")

@app.on_message(filters.command("stop") & filters.group)
@filters.create(is_admin)
async def stop_cmd(client, message):
    if message.chat.id in player.active_chats:
        await player.stop(call_py, message.chat.id)
        await message.reply("⏹ Stopped.\n🔇 **ROSE** ne voice chat chhod di. 🍬")
        await send_log(client, f"⏹ Stop by {message.from_user.mention} in {message.chat.title} [{message.chat.id}]")
    else:
        await message.reply("❌ Not in voice chat.")
