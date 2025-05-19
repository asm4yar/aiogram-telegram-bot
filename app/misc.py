from datetime import datetime
from typing import Union

from aiogram.enums import ChatAction
from aiogram.types import Message, CallbackQuery

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


async def safe_send_photo(update: Union[CallbackQuery | Message], caption, photo, params: dict = None):
    params = params or {}
    message = update.message if isinstance(update, CallbackQuery) else update

    if len(caption) <= MAX_CAPTION_LENGTH:
        await message.answer_photo(photo=photo, caption=caption, **params)
    else:
        await message.answer_photo(photo)
        await message.answer(caption, **params)
