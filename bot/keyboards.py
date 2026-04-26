from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .fonts import premium

def player_keyboard(duration: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏪ 10s", callback_data="seek:-10"),
            InlineKeyboardButton("⏸ " + premium("pause"), callback_data="pause"),
            InlineKeyboardButton("10s ⏩", callback_data="seek:10"),
        ],
        [
            InlineKeyboardButton("▶️ " + premium("play"), callback_data="resume"),
            InlineKeyboardButton("⏹ " + premium("stop"), callback_data="stop"),
        ],
        [InlineKeyboardButton("⏱ " + duration, callback_data="duration")],
    ])

def start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ " + premium("add me"), url="https://t.me/YourBotUsername?startgroup=true")],
        [InlineKeyboardButton("❖ " + premium("help menu"), callback_data="help")],
    ])
