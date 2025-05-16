import re

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from classes import gpt_client
from classes.chat_gpt import GPTMessage
from classes.resource import Resource, Button, TrainingWords
from config import GPTRole, VOCAB_LANG, FSMKey
from keyboards.callback_data import CelebrityData, QuizData, VocabData
from keyboards.inline_keyboards import ikb_vocab_training_management
from misc import lang_is_allow
from .command import com_start, com_quiz, com_vocab
from .handlers import training_handler
from .handlers_state import CelebrityTalk, Quiz, Vocab

callback_router = Router()


@callback_router.callback_query(CelebrityData.filter(F.button == 'select_celebrity'))
async def celebrity_callbacks(callback: CallbackQuery, callback_data: CelebrityData, bot: Bot, state: FSMContext):
    photo = Resource(callback_data.file_name).photo
    button_name = Button.from_file(callback_data.file_name).name
    await callback.answer(
        text=f'С тобой говорит {button_name}',
    )
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption='Задайте свой вопрос:',
    )
    request_message = GPTMessage(callback_data.file_name)
    await state.set_state(CelebrityTalk.wait_for_answer)
    await state.set_data({'messages': request_message, 'photo': photo})


@callback_router.callback_query(QuizData.filter(F.button == 'select_topic'))
async def select_topic(callback: CallbackQuery, callback_data: QuizData, bot: Bot, state: FSMContext):
    photo = Resource('quiz').photo
    await callback.answer(
        text=f'Вы выбрали тему {callback_data.topic_name}!',
    )
    request_message = GPTMessage('quiz')
    request_message.update(GPTRole.USER, callback_data.topic)
    response = await gpt_client.request(request_message)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption=response,
    )
    await state.set_state(Quiz.wait_for_answer)
    request_message.update(GPTRole.ASSISTANT, response)
    await state.set_data({'messages': request_message, 'photo': photo, 'score': 0, 'callback': callback_data})


@callback_router.callback_query(QuizData.filter(F.button == 'next_question'))
async def quiz_next_question(callback: CallbackQuery, state: FSMContext):
    data: dict[str, GPTMessage | str | QuizData] = await state.get_data()
    await callback.answer(
        text=f'Продолжаем тему {data['callback'].topic_name}'
    )
    data['messages'].update(GPTRole.USER, 'quiz_more')
    response = await gpt_client.request(data['messages'])
    data['messages'].update(GPTRole.ASSISTANT, response)
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=data['photo'],
        caption=response,
    )
    await state.set_state(Quiz.wait_for_answer)
    await state.update_data(data)


@callback_router.callback_query(QuizData.filter(F.button == 'finish_quiz'))
async def finish_quiz(callback: CallbackQuery, state: FSMContext):
    await callback.answer(
        text=f'Вы выбрали закончить!',
    )
    await state.clear()
    await com_start(callback.message)


@callback_router.callback_query(QuizData.filter(F.button == 'change_topic'))
async def change_topic(callback: CallbackQuery, state: FSMContext):
    await callback.answer(
        text=f'Вы выбрали сменить тему!',
    )

    await state.set_state(Quiz.wait_for_answer)
    await com_quiz(callback.message)


@callback_router.callback_query(VocabData.filter(F.button == 'vocab_words'))
async def vocab_words(callback: CallbackQuery, callback_data: VocabData, state: FSMContext):
    lang_id = callback_data.lang_id
    if not lang_is_allow(lang_id):
        lang_id = 0

    await callback.answer('')

    cur_state = await state.get_state()
    if cur_state != Vocab.words:
        await state.clear()
        await com_vocab(callback.message, state)
        return

    data: dict = await state.get_data()
    gpt_message: GPTMessage = data.get('messages', GPTMessage('vocab'))
    training_words: list = data.get(FSMKey.TRAINING_WORDS.value, [])

    lang = VOCAB_LANG[lang_id].language
    flag = VOCAB_LANG[lang_id].flag

    gpt_message.update(GPTRole.USER, 'vocab_more {{lang}}'.replace('lang', lang))

    response_vocab_word = await gpt_client.request(gpt_message)

    match = re.search(r"#(.+)→(.+)#", response_vocab_word)
    if not match:
        await callback.answer('Попробуйте еще раз...', show_alert=True)
        return

    word = match.group(1).strip()
    word_translate = match.group(2).strip()
    training_word = TrainingWords(word=word, word_translate=word_translate, lang_id=lang_id)
    training_words.append(training_word)

    updated_response = re.sub(r"#(.+)→(.+)#", f"{word} → {word_translate}", response_vocab_word)
    gpt_message.update(GPTRole.ASSISTANT, response_vocab_word)

    await state.update_data({'messages': gpt_message, FSMKey.TRAINING_WORDS.value: training_words})

    saved_message_id = data.get(FSMKey.VOCAB_MESSAGE_ID.value)
    chat_id = callback.message.chat.id
    to_message = {'text': f'{flag} {updated_response}', 'reply_markup': ikb_vocab_training_management(lang_id)}

    if saved_message_id:
        try:
            await callback.bot.edit_message_text(**to_message, message_id=saved_message_id, chat_id=chat_id)
        except Exception as _:
            sent_message = await callback.message.answer(**to_message)
            await state.update_data({FSMKey.VOCAB_MESSAGE_ID.value: sent_message.message_id})

    else:
        sent_message = await callback.message.answer(**to_message)
        await state.update_data({FSMKey.VOCAB_MESSAGE_ID.value: sent_message.message_id})

    await state.set_state(Vocab.words)


@callback_router.callback_query(VocabData.filter(F.button == 'vocab_finish'))
async def vocab_finish(callback: CallbackQuery, callback_data: VocabData, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await com_start(callback.message)


@callback_router.callback_query(VocabData.filter(F.button == 'vocab_training'))
async def vocab_training(callback: CallbackQuery, callback_data: VocabData, state: FSMContext):
    current_state = await state.get_state()
    if current_state != Vocab.words.state:
        await restart_vocab_training(callback, state)
        return

    data: dict = await state.get_data()
    training_words: list[TrainingWords] = data.get(FSMKey.TRAINING_WORDS.value, [])
    if 0 == len(training_words):
        await restart_vocab_training(callback, state)

    await training_handler(callback, state)


async def restart_vocab_training(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Начнём сначала!", show_alert=True)
    await com_vocab(callback.message, state)
