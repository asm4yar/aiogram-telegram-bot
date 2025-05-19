from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from classes import gpt_client
from classes.chat_gpt import GPTMessage, GPTRole
from classes.resource import Resource, Translator
from config import FSMKey
from keyboards import kb_end_talk, ikb_quiz_next
from keyboards.callback_data import QuizData
from keyboards.inline_keyboards import translate_change_finish
from misc import bot_thinking, custom_replace, safe_send_photo
from .command import com_start, com_translator
from .handlers import training_handler, handle_possible_command
from .handlers_state import CelebrityTalk, ChatGPTRequests, Quiz, Vocab, TranslatorState

message_router = Router()


@message_router.message(CelebrityTalk.wait_for_answer, F.text == 'Попрощаться!')
async def end_talk_handler(message: Message, state: FSMContext):
    await state.clear()
    await com_start(message, state)


@message_router.message(ChatGPTRequests.wait_for_request)
async def wait_for_gpt_handler(message: Message, state: FSMContext):
    if await handle_possible_command(message, state):
        return
    await bot_thinking(message)
    gpt_message = GPTMessage('gpt')
    gpt_message.update(GPTRole.USER, message.text)
    gpt_response = await gpt_client.request(gpt_message)
    photo = Resource('gpt').photo
    await safe_send_photo(message, photo=photo, caption=gpt_response)
    await state.clear()


@message_router.message(CelebrityTalk.wait_for_answer)
async def talk_handler(message: Message, state: FSMContext):
    if await handle_possible_command(message, state):
        return
    await bot_thinking(message)
    data: dict[str, GPTMessage | str] = await state.get_data()
    data['messages'].update(GPTRole.USER, message.text)
    gpt_response = await gpt_client.request(data['messages'])
    await safe_send_photo(message, photo=data['photo'], caption=gpt_response, params={'reply_markup': kb_end_talk()})
    data['messages'].update(GPTRole.ASSISTANT, gpt_response)
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
    await safe_send_photo(
        message,
        photo=data['photo'],
        caption=f'Ваш счёт: {data["score"]}\n{response}',
        params={'reply_markup': ikb_quiz_next(data['callback'])}
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

    await safe_send_photo(
        message,
        photo=photo,
        caption=f'Ваш счёт: {score}\n{last_response}',
        params={'reply_markup': ikb_quiz_next(callback_data)}
    )

@message_router.message(Vocab.message_training)
async def process_vocab_answer(message: Message, state: FSMContext):
    await training_handler(message, state)


@message_router.message(TranslatorState.wait_user_message)
async def process_translator_answer(message: Message, state: FSMContext):
    if await handle_possible_command(message, state):
        return
    data = await state.get_data()
    translator: Translator = data.get(FSMKey.TRANSLATOR.value)
    if translator is None:
        await com_translator(message)
        return

    request_message = GPTMessage('translator', custom_replace('{{lang}}', translator.lang.lower()))
    request_message.update(GPTRole.USER, message.text)
    gpt_response = await gpt_client.request(request_message)
    await message.answer(gpt_response, reply_markup=translate_change_finish())
