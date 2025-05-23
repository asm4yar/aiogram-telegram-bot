from typing import Type

from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.resource import Buttons, Button
from config import LANGS
from .callback_data import CelebrityData, QuizData, VocabData, BaseLangData, TranslatorData


def ikb_celebrity():
    keyboard = InlineKeyboardBuilder()
    buttons = Buttons()
    for button in buttons:
        keyboard.button(
            text=button.name,
            callback_data=CelebrityData(
                button='select_celebrity',
                file_name=button.callback,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_quiz_select_topic():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Язык Python', 'quiz_prog'),
        Button('Математика', 'quiz_math'),
        Button('Биология', 'quiz_biology'),
    ]
    for button in buttons:
        keyboard.button(
            text=button.name,
            callback_data=QuizData(
                button='select_topic',
                topic=button.callback,
                topic_name=button.name,
            )

        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_quiz_next(current_topic: QuizData):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Дальше', 'next_question'),
        Button('Сменить тему', 'change_topic'),
        Button('Закончить', 'finish_quiz'),
    ]

    for button in buttons:
        keyboard.button(
            text=button.name,
            callback_data=QuizData(
                button=button.callback,
                topic=current_topic.topic,
                topic_name=current_topic.topic_name
            )
        )
    keyboard.adjust(2, 1)
    return keyboard.as_markup()

def ikb_select_lang(callback_cls: Type[BaseLangData], button_value: str):
    keyboard = InlineKeyboardBuilder()

    for lang_id, btn in enumerate(LANGS):
        keyboard.button(
            text=f"{btn.flag} {btn.language}",
            callback_data=callback_cls(
                button=button_value,
                lang_id=lang_id,
            )
        )

    keyboard.adjust(1)
    return keyboard.as_markup()

def translate_change_finish():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Сменить язык', TranslatorData(button='com_translator')),
        Button('Закончить', TranslatorData(button='translator_finish')),
    ]
    for button in buttons:
        keyboard.button(
            text=button.name,
            callback_data=button.callback
        )
    keyboard.adjust(2)
    return keyboard.as_markup()


def ikb_vocab_training_management(lang_id):
    keyboard = InlineKeyboardBuilder()

    buttons = [
        Button('Ещё слово', VocabData(button='vocab_words', lang_id=lang_id)),
        Button('Тренироваться', VocabData(button='vocab_training')),
        Button('Закончить', VocabData(button='vocab_finish')),
    ]

    for button in buttons:
        keyboard.button(
            text=button.name,
            callback_data=button.callback
        )
    keyboard.adjust(2, 1)
    return keyboard.as_markup()
