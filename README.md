# Premium Telegram VC Music Bot

Telegram Bot API alone voice chat join nahi kar sakta. VC/group call music stream ke liye **bot token + assistant user session** chahiye.

## Features
- Premium small-caps font messages: `sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ`
- `/start`, `/help`, `/play <song name | YouTube URL | Spotify URL>`
- YouTube search/download via `yt-dlp`
- Spotify link support via `spotdl` fallback
- Inline buttons: play/resume, pause, stop, 10s back, 10s forward
- Thumbnail + duration message
- Welcome image support
- Spoiler/blur photo helper command: `/photo` reply to an image

## Requirements
- Python 3.10+
- FFmpeg installed
- Telegram `API_ID` and `API_HASH` from https://my.telegram.org
- Bot token from @BotFather
- Assistant user session string generated with Pyrogram

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python generate_session.py
python main.py
```

## Important
1. Add both bot and assistant account to your group/channel.
2. Make bot admin.
3. Start voice chat manually in group/channel, then use `/play song name`.
4. Put generated session string in `.env` as `ASSISTANT_SESSION`.

## Commands
```text
/start
/help
/play alone alan walker
/play https://www.youtube.com/watch?v=...
/pause
/resume
/stop
/seek 10
/seek -10
/photo   reply this command to a photo to resend it blurred/spoiler
```
