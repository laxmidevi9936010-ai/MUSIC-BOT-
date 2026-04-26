import os
import asyncio
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID", "35828291"))
API_HASH = os.environ.get("API_HASH", "c025ee9d01d73b9d738d4f3e5e6137e2")
BOT_TOKEN = os.environ.get("8631333041:AAHWj3Ut17BSn4laROufER6gF24eA0Hqj2c", "")
ASSISTANT_SESSION = os.environ.get("ASSISTANT_SESSION", "BQIiskMAVA6lEUPzkmTtQn7zh__KAJn0nzSuebU2tw30rtVbz4Tq4Ai03em8OlirqyZxa2ZNAgY2SBf87wY4hsiBin7uN7SYE6y4JSWtzKnGep3IfQe3rJE2-iGE1-0loCRhLLs_ZduSfyTIR7JXFP984-1_ZTwDQu_dGEXpc2a_2acwT4skZRj8mHUgT1SKW5JtEpf3CA8e2xiazKVHtz-jUI7w1wLHpQBm9iUGoaQ9poZQeMt1D8FhIDO335CzgUlwpZkYZ7B_gPg7gPXKfuz9V0OqFEYnZ5pYTNwRM45fWx_ozUfnNP8HAeJLhGRtGPtJeyI0Qyygui_2YSjjQ-Zd6vh5cQAAAAIHIiSYAA")
OWNER_ID = int(os.environ.get("OWNER_ID", "7953454559"))

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

assistant = None
if ASSISTANT_SESSION:
    assistant = Client(
        "assistant",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=ASSISTANT_SESSION,
    )

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Bot Railway par successfully running hai ✅")

@bot.on_message(filters.command("ping"))
async def ping(_, message):
    await message.reply_text("Pong ✅")

async def main():
    if assistant:
        await assistant.start()
        print("Assistant started")
    await bot.start()
    print("Bot started")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
