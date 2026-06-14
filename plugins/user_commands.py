from pyrogram import Client, filters
from main import app, user, call_py
from utils.yt_utils import get_audio_url, get_video_url
from music.player import player
from utils.logger import send_log
from config import THUMBNAIL_URL

async def ensure_voice_chat(client, chat_id):
    try: await client.get_group_call(chat_id)
    except: await client.create_group_call(chat_id)

@app.on_message(filters.command("play") & filters.group)
async def user_play(client, message):
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
    await send_log(client, f"👤 /play: {title} by {message.from_user.mention}")

@app.on_message(filters.command("vplay") & filters.group)
async def user_vplay(client, message):
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
    await send_log(client, f"👤 /vplay: {title} by {message.from_user.mention}")
