from abc import ABC

from aiogram.filters.callback_data import CallbackData


class CelebrityData(CallbackData, prefix='_CD'):
    button: str
    file_name: str


class QuizData(CallbackData, prefix='_QD'):
    button: str
    topic: str
    topic_name: str


class BaseLangData(CallbackData, ABC, prefix="base_unused"):
    button: str


class VocabData(BaseLangData, prefix="_VB"):
    lang_id: int | None = None


class TranslatorData(BaseLangData, prefix="_TR"):
    lang_id: int | None = None
