from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import app, user, call_py
from music.player import player
from config import SUPPORT_LINK, UPDATE_LINK, OWNER_LINK, SOURCE_LINK
from utils.logger import send_log

FANCY_NAME = "🌸 ᥀꯭🦄ุᮀ̶⃝꯭჻꯭꯭𝐑꯭꯭꯭꯭ ⃪𝐎꯭꯭꯭꯭ ⃪֟፝͝𝐒꯭꯭꯭꯭ ⃪𝐄⃪꯭꯭꯭꯭🍬᥀꯭჻꯭꯭𝐗⃪꯭꯭꯭꯭🍬᥀꯭⃝꯭჻꯭꯭𝐌꯭꯭꯭꯭ ⃪𝐮꯭꯭꯭꯭ ⃪֟፝͝𝐬꯭꯭꯭꯭ ⃪𝛊꯭꯭꯭꯭ ⃪𝐜⃪꯭꯭꯭꯭🍬⃝゚⃞꯭࿐"

WELCOME_TEXT = f"""{FANCY_NAME}

✨ Welcome, {{mention}} to **{{chat_title}}**!
🎶 I'm ROSE Music Bot – let's rock the voice chat! ❤️‍🔥
Use /help to see commands."""

VOICE_START_TEXT = "🎤 **ROSE** aa gayi! Voice chat shuru, ho jao taiyar! ❤️‍🔥"
VOICE_END_TEXT = "🔇 **ROSE** ruk gayi. Phir milenge! 🍬"

HELP_TEXT = """🌹 **ROSE Music Bot** Commands:

👤 **All Users:**
/play <song> - Play audio
/vplay <video> - Stream video

🛡 **Admins:**
/skip, /end, /pause, /resume, /stop
/ban, /mute, /unban, /unmute

👑 **Owner:**
All commands + /broadcast, /pmcast, /stats
/gban, /gunban, /banall"""

KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("📣 Support", url=SUPPORT_LINK),
     InlineKeyboardButton("🔔 Updates", url=UPDATE_LINK)],
    [InlineKeyboardButton("👑 Owner", url=OWNER_LINK),
     InlineKeyboardButton("📂 Source Code", url=SOURCE_LINK)]
])

@app.on_chat_member_updated()
async def welcome_new_member(client, event):
    if event.new_chat_member and event.new_chat_member.user.id != (await client.get_me()).id:
        user_member = event.new_chat_member.user
        chat = event.chat
        mention = f"<a href='tg://user?id={user_member.id}'>{user_member.first_name}</a>"
        await client.send_message(chat.id, WELCOME_TEXT.format(mention=mention, chat_title=chat.title), disable_web_page_preview=True)
        await send_log(client, f"👋 New member {user_member.mention} joined {chat.title} [{chat.id}]")

@app.on_message(filters.voice_chat_started)
async def voice_start(client, message):
    await message.reply(VOICE_START_TEXT)
    await send_log(client, f"🎤 Voice chat started in {message.chat.title} [{message.chat.id}]")

@app.on_message(filters.voice_chat_ended)
async def voice_end(client, message):
    await message.reply(VOICE_END_TEXT)
    await send_log(client, f"🔇 Voice chat ended in {message.chat.title} [{message.chat.id}]")

@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    await message.reply(HELP_TEXT, reply_markup=KEYBOARD)
    await send_log(client, f"❓ /help by {message.from_user.mention}")

@call_py.on_stream_end()
async def stream_end(client, update):
    chat_id = update.chat_id
    try:
        next_title = await player.play_next(user, call_py, chat_id)
        if next_title:
            await app.send_message(chat_id, f"⏭ Now playing: **{next_title}**")
            await send_log(app, f"⏭ Auto-play next: {next_title} in chat {chat_id}")
        else:
            await player.stop(call_py, chat_id)
            await app.send_message(chat_id, VOICE_END_TEXT)
            await send_log(app, f"🔇 Queue empty, stopped in chat {chat_id}")
    except Exception as e:
        print(f"Stream end error: {e}")
        await send_log(app, f"⚠️ Stream end error in chat {chat_id}: {e}")
