from aiogram.filters.callback_data import CallbackData


class CelebrityData(CallbackData, prefix='_CD'):
    button: str
    file_name: str


class QuizData(CallbackData, prefix='_QD'):
    button: str
    topic: str
    topic_name: str


class VocabData(CallbackData, prefix='_VB'):
    button: str
    lang_id: int | None = None
