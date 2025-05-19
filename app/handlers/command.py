from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from classes import gpt_client
from classes.chat_gpt import GPTMessage
from classes.resource import Resource
from keyboards import kb_reply, ikb_celebrity, ikb_quiz_select_topic, ikb_select_lang
from keyboards.callback_data import VocabData, TranslatorData
from misc import bot_thinking, safe_send_photo
from .handlers_state import ChatGPTRequests, Vocab

command_router = Router()


@command_router.message(F.text == 'Закончить')
@command_router.message(Command('start'))
async def com_start(message: Message, state: FSMContext):
    await state.clear()
    resource = Resource('main')
    buttons = [
        '/random',
        '/gpt',
        '/talk',
        '/quiz',
        '/vocab',
        '/translator'
    ]
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=kb_reply(buttons),
    )


@command_router.message(F.text == 'Хочу еще факт')
@command_router.message(Command('random'))
async def com_random(message: Message):
    await bot_thinking(message)
    resource = Resource('random')
    gpt_message = GPTMessage('random')
    buttons = [
        'Хочу еще факт',
        'Закончить',
    ]
    msg_text = await gpt_client.request(gpt_message)
    await safe_send_photo(
        message,
        photo=resource.photo,
        caption=msg_text,
        params={'reply_markup': kb_reply(buttons)}
    )


@command_router.message(Command('gpt'))
async def com_gpt(message: Message, state: FSMContext):
    await state.set_state(ChatGPTRequests.wait_for_request)
    await bot_thinking(message)
    resource = Resource('gpt')
    await safe_send_photo(
        message,
        **resource.as_kwargs(),
    )


@command_router.message(Command('talk'))
async def com_talk(message: Message):
    await bot_thinking(message)
    resource = Resource('talk')
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=ikb_celebrity(),
    )


@command_router.message(Command('quiz'))
async def com_quiz(message: Message):
    await bot_thinking(message)
    resource = Resource('quiz')
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=ikb_quiz_select_topic(),
    )


@command_router.message(Command('vocab'))
async def com_vocab(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Vocab.words)
    await bot_thinking(message)
    resource = Resource('vocab')
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=ikb_select_lang(VocabData, 'vocab_words'),
    )

    # translator
@command_router.message(Command('translator'))
async def com_translator(message: Message, state: FSMContext):
    await state.clear()
    await bot_thinking(message)
    resource = Resource('translator')
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=ikb_select_lang(TranslatorData, 'translator'),
    )
