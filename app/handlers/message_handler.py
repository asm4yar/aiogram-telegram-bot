import random

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from classes import gpt_client
from classes.chat_gpt import GPTMessage, GPTRole
from classes.resource import Resource
from keyboards import kb_end_talk, ikb_quiz_next
from keyboards.callback_data import QuizData
from misc import bot_thinking, custom_replace
from .command import com_start, com_quiz, com_vocab, com_talk, com_gpt, com_random
from .handlers import training_handler
from .handlers_state import CelebrityTalk, ChatGPTRequests, Quiz, Vocab

message_router = Router()


async def handle_possible_command(message: Message, state: FSMContext) -> bool:
    """
    Проверяет, является ли сообщение командой. Если да — сбрасывает состояние и вызывает нужный хендлер.
    Возвращает True, если команда была обработана, иначе False.
    """
    if not message.text or not message.text.startswith('/'):
        return False

    await state.clear()

    command_map = {
        '/start': com_start,
        '/quiz': com_quiz,
        '/vocab': com_vocab,
        '/talk': com_talk,
        '/gpt': com_gpt,
        '/random': com_random,
    }

    handler = command_map.get(message.text.split()[0])
    if handler:
        # Передаём state только если требуется
        if handler.__code__.co_argcount == 2:
            await handler(message, state)
        else:
            await handler(message)
    else:
        await message.answer("Команда не распознана. Используйте /start для начала.")
    return True


@message_router.message(CelebrityTalk.wait_for_answer, F.text == 'Попрощаться!')
async def end_talk_handler(message: Message, state: FSMContext):
    await state.clear()
    await com_start(message)


@message_router.message(ChatGPTRequests.wait_for_request)
async def wait_for_gpt_handler(message: Message, state: FSMContext):
    if await handle_possible_command(message, state):
        return
    await bot_thinking(message)
    gpt_message = GPTMessage('gpt')
    gpt_message.update(GPTRole.USER, message.text)
    gpt_response = await gpt_client.request(gpt_message)
    photo = Resource('gpt').photo
    await message.answer_photo(
        photo=photo,
        caption=gpt_response,
    )
    await state.clear()


@message_router.message(CelebrityTalk.wait_for_answer)
async def talk_handler(message: Message, state: FSMContext):
    if await handle_possible_command(message, state):
        return
    await bot_thinking(message)
    data: dict[str, GPTMessage | str] = await state.get_data()
    data['messages'].update(GPTRole.USER, message.text)
    response = await gpt_client.request(data['messages'])
    await message.answer_photo(
        photo=data['photo'],
        caption=response,
        reply_markup=kb_end_talk(),
    )
    data['messages'].update(GPTRole.ASSISTANT, response)
    await state.update_data(data)


@message_router.message(Quiz.wait_for_answer)
async def quiz_answer(message: Message, state: FSMContext):
    if await handle_possible_command(message, state):
        return
    data: dict[str, GPTMessage | str | QuizData] = await state.get_data()

    # Обновляем историю сообщений
    data['messages'].update(GPTRole.USER, message.text)
    response = await gpt_client.request(data['messages'])

    # Сохраняем последний ответ
    data['last_response'] = response

    # Проверяем ответ
    if response == 'Правильно!':
        data['score'] += 1
    elif response.startswith('Неправильно'):
        pass
    else:
        # Если GPT среагировал вне формата, напомним про команды
        await message.answer("Пожалуйста, используйте кнопки: Далее, Сменить тему или Закончить.")
        return

    data['messages'].update(GPTRole.ASSISTANT, response)

    # Отправляем результат с кнопками
    await message.answer_photo(
        photo=data['photo'],
        caption=f'Ваш счёт: {data["score"]}\n{response}',
        reply_markup=ikb_quiz_next(data['callback']),  # Далее / Сменить тему / Закончить
    )

    # Устанавливаем состояние ожидания нажатия кнопки, а не ввода текста
    await state.set_state(Quiz.wait_for_next_action)
    await state.update_data(data)


@message_router.message(Quiz.wait_for_next_action)
async def block_extra_input(message: Message, state: FSMContext):
    if await handle_possible_command(message, state):
        return
    data: dict[str, GPTMessage | str | QuizData] = await state.get_data()
    score = data.get('score', 0)
    last_response = data.get('last_response', 'Ожидание ответа...')  # Если нет ответа, отображаем это
    photo = data['photo']
    callback_data = data['callback']

    await message.answer_photo(
        photo=photo,
        caption=f'Ваш счёт: {score}\n{last_response}',
        reply_markup=ikb_quiz_next(callback_data),
    )


@message_router.message(Vocab.message_training)
async def process_vocab_answer(message: Message, state: FSMContext):
    await training_handler(message, state)
