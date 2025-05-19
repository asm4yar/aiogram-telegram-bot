import random
from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from classes import gpt_client
from classes.chat_gpt import GPTMessage
from classes.resource import TrainingWords
from config import GPTRole, FSMKey
from misc import custom_replace
from .command import com_start, com_quiz, com_vocab, com_talk, com_gpt, com_random, com_translator
from .handlers_state import Vocab


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
        '/translator': com_translator,
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


async def training_handler(update: Union[CallbackQuery, Message], state: FSMContext):
    if isinstance(update, CallbackQuery):
        data = await state.get_data()
        chat_id = update.message.chat.id
        saved_message_id = data.get(FSMKey.VOCAB_MESSAGE_ID.value)
        if saved_message_id:
            try:
                await update.bot.edit_message_text(text='Тренировка начата!', chat_id=chat_id,
                                                   message_id=saved_message_id)
            except Exception as _:
                await update.message.answer(text='Тренировка начата!')

        training = await pop_and_set_cur_item(state)
        await state.set_state(Vocab.message_training)
        await update.message.answer(f'Напишите перевод слова {training.flag} {training.word}')
        return

    if isinstance(update, Message):
        prev_training = await pop_and_set_cur_item(state, return_only=True)
        if not prev_training:
            await com_start(update, state)
            return

        if await handle_possible_command(update, state):
            return

        gpt_message: GPTMessage = GPTMessage('vocab_training', custom_replace('{{lang}}', prev_training.lang))
        gpt_message.update(GPTRole.ASSISTANT, f'{prev_training.word} - {prev_training.word_translate}')
        gpt_message.update(GPTRole.USER, f'{update.text}')
        response_vocab_word = await gpt_client.request(gpt_message)

        is_correct = response_vocab_word.startswith('Правильно!')
        await update_counter(state, is_correct)

        if await allow_next_training(state):
            training = await pop_and_set_cur_item(state)
            await update.answer(f'Напишите перевод слова {training.flag} {training.word}')
        else:
            counter_success, counter_total = await get_counter(state)
            await update.answer(f'Тренировка завершена! Ваш результат: {counter_success}/{counter_total}')
            await state.clear()
            await com_start(update, state)


async def update_counter(state: FSMContext, is_correct: bool) -> None:
    data = await state.get_data()
    counter_success = data.get(FSMKey.COUNTER_SUCCESS.value, 0)
    counter_total = data.get(FSMKey.COUNTER_TOTAL.value, 0)
    counter_total += 1
    if is_correct:
        counter_success += 1

    await state.update_data({
        FSMKey.COUNTER_SUCCESS.value: counter_success,
        FSMKey.COUNTER_TOTAL.value: counter_total,
    })


async def get_counter(state: FSMContext) -> tuple[int, int]:
    data = await state.get_data()
    return (
        data.get(FSMKey.COUNTER_SUCCESS.value, 0),
        data.get(FSMKey.COUNTER_TOTAL.value, 0)
    )


async def pop_and_set_cur_item(state: FSMContext, return_only=False):
    data = await state.get_data()
    item_list = data.get(FSMKey.TRAINING_WORDS.value, [])
    previous_item: TrainingWords | None = data.get(FSMKey.TRAINING_CURRENT.value)

    if return_only:
        return previous_item

    if not item_list:
        return None

    random_key = random.randrange(len(item_list))
    random_item = item_list.pop(random_key)

    await state.update_data({
        FSMKey.TRAINING_WORDS.value: item_list,
        FSMKey.TRAINING_CURRENT.value: random_item
    })

    return random_item


async def allow_next_training(state: FSMContext):
    data = await state.get_data()
    item_list = data.get(FSMKey.TRAINING_WORDS.value)
    return isinstance(item_list, list) and len(item_list) > 0
