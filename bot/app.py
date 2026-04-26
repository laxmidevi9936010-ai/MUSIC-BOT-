import os
from dotenv import load_dotenv
from pyrogram import Client, filters, idle
from pyrogram.types import Message, CallbackQuery
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from .downloader import get_track, human_time
from .fonts import premium, box
from .keyboards import player_keyboard, start_keyboard
from .welcome_image import ensure_welcome_image

load_dotenv()
API_ID = int(os.getenv("API_ID", "35828291"))
API_HASH = os.getenv("API_HASH", "c025ee9d01d73b9d738d4f3e5e6137e2")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8631333041:AAHWj3Ut17BSn4laROufER6gF24eA0Hqj2c")
ASSISTANT_SESSION = os.getenv("ASSISTANT_SESSION", "BQIiskMAVA6lEUPzkmTtQn7zh__KAJn0nzSuebU2tw30rtVbz4Tq4Ai03em8OlirqyZxa2ZNAgY2SBf87wY4hsiBin7uN7SYE6y4JSWtzKnGep3IfQe3rJE2-iGE1-0loCRhLLs_ZduSfyTIR7JXFP984-1_ZTwDQu_dGEXpc2a_2acwT4skZRj8mHUgT1SKW5JtEpf3CA8e2xiazKVHtz-jUI7w1wLHpQBm9iUGoaQ9poZQeMt1D8FhIDO335CzgUlwpZkYZ7B_gPg7gPXKfuz9V0OqFEYnZ5pYTNwRM45fWx_ozUfnNP8HAeJLhGRtGPtJeyI0Qyygui_2YSjjQ-Zd6vh5cQAAAAIHIiSYAA")

if not all([API_ID, API_HASH, BOT_TOKEN, ASSISTANT_SESSION]):
    raise SystemExit(".env me API_ID, API_HASH, BOT_TOKEN, ASSISTANT_SESSION sab bharna zaroori hai.")

bot = Client("premium_music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
assistant = Client("assistant", api_id=API_ID, api_hash=API_HASH, session_string=ASSISTANT_SESSION)
call = PyTgCalls(assistant)
CURRENT = {}

HELP_TEXT = """
/play <song name> - gana search karke vc me stream karega
/pause - song pause
/resume - song resume
/stop - vc stream stop
/seek 10 - 10 seconds aage
/seek -10 - 10 seconds piche
/photo - kisi photo pe reply karke spoiler blur me resend
""".strip()

@bot.on_message(filters.command("start"))
async def start(_, m: Message):
    photo = ensure_welcome_image()
    await m.reply_photo(
        photo,
        caption=box("started successfully", "premium vc music bot ready hai. group ya channel me voice chat start karke /play <song name> bhejo."),
        reply_markup=start_keyboard(),
    )

@bot.on_message(filters.command("help"))
async def help_cmd(_, m: Message):
    await m.reply_text(box("help menu", HELP_TEXT), reply_markup=start_keyboard())

@bot.on_message(filters.command("play"))
async def play_cmd(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(box("send song name", "/play <song_name>"))
    query = m.text.split(maxsplit=1)[1]
    status = await m.reply_text(box("searching", f"{query}"))
    try:
        track = await get_track(query)
        chat_id = m.chat.id
        await call.join_group_call(chat_id, AudioPiped(track["file"]))
        CURRENT[chat_id] = track
        duration = human_time(track.get("duration"))
        caption = box(
            "vc start now ok",
            f"title: {track['title']}\nduration: {duration}\nsource: {track.get('webpage_url', '')}"
        )
        if track.get("thumbnail"):
            await status.delete()
            await m.reply_photo(track["thumbnail"], caption=caption, reply_markup=player_keyboard(duration))
        else:
            await status.edit_text(caption, reply_markup=player_keyboard(duration))
    except Exception as e:
        await status.edit_text(box("error", str(e)[:900]))

@bot.on_message(filters.command("pause"))
async def pause_cmd(_, m: Message):
    await call.pause_stream(m.chat.id)
    await m.reply_text(box("paused"))

@bot.on_message(filters.command("resume"))
async def resume_cmd(_, m: Message):
    await call.resume_stream(m.chat.id)
    await m.reply_text(box("playing now"))

@bot.on_message(filters.command("stop"))
async def stop_cmd(_, m: Message):
    await call.leave_group_call(m.chat.id)
    CURRENT.pop(m.chat.id, None)
    await m.reply_text(box("stopped successfully"))

@bot.on_message(filters.command("seek"))
async def seek_cmd(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(box("usage", "/seek 10 or /seek -10"))
    seconds = int(m.command[1])
    await call.change_stream(m.chat.id, AudioPiped(CURRENT[m.chat.id]["file"], additional_ffmpeg_parameters=f"-ss {max(seconds, 0)}"))
    await m.reply_text(box("seek updated", f"{seconds} seconds"))

@bot.on_message(filters.command("photo") & filters.reply)
async def spoiler_photo(_, m: Message):
    if not (m.reply_to_message and m.reply_to_message.photo):
        return await m.reply_text(box("reply to photo", "photo pe reply karke /photo bhejo."))
    file_id = m.reply_to_message.photo.file_id
    await m.reply_photo(file_id, caption=premium("tap to reveal"), has_spoiler=True)

@bot.on_callback_query()
async def callbacks(_, q: CallbackQuery):
    data = q.data or ""
    chat_id = q.message.chat.id
    try:
        if data == "help":
            await q.message.edit_caption(box("help menu", HELP_TEXT), reply_markup=start_keyboard()) if q.message.caption else await q.message.edit_text(box("help menu", HELP_TEXT), reply_markup=start_keyboard())
        elif data == "pause":
            await call.pause_stream(chat_id)
            await q.answer(premium("paused"), show_alert=False)
        elif data == "resume":
            await call.resume_stream(chat_id)
            await q.answer(premium("playing"), show_alert=False)
        elif data == "stop":
            await call.leave_group_call(chat_id)
            CURRENT.pop(chat_id, None)
            await q.message.edit_caption(box("stopped successfully")) if q.message.caption else await q.message.edit_text(box("stopped successfully"))
        elif data.startswith("seek:"):
            seconds = int(data.split(":", 1)[1])
            await q.answer(premium(f"seek {seconds}s"), show_alert=False)
        else:
            await q.answer(premium("track duration"), show_alert=False)
    except Exception as e:
        await q.answer(str(e)[:180], show_alert=True)

async def start_bot():
    await assistant.start()
    await call.start()
    await bot.start()
    me = await bot.get_me()
    print(premium(f"started successfully: @{me.username}"))
    await idle()
    await bot.stop()
    await call.stop()
    await assistant.stop()
