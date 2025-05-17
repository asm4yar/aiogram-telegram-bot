from datetime import datetime

from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.types import Message

from config import LANGS, MAX_CAPTION_LENGTH


def on_start():
    time_now = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
    print(f'Bot is started at {time_now}')


def on_shutdown():
    time_now = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
    print(f'Bot is down at {time_now}')


async def bot_thinking(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )


def custom_replace(_old: str, _new: str):
    def replace_prompt(text: str) -> str:
        return text.replace(_old, _new)

    return replace_prompt


def lang_is_allow(lang_id):
    return 0 <= lang_id < len(LANGS)

async def safe_send_photo(bot: Bot, chat_id: int, photo: str, caption: str = ""):
    if caption and len(caption) <= MAX_CAPTION_LENGTH:
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
    else:
        await bot.send_photo(chat_id=chat_id, photo=photo)
        await bot.send_message(chat_id=chat_id, text=caption)

