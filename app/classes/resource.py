import os
from dataclasses import dataclass
from aiogram.filters.callback_data import CallbackData
from aiogram.types import FSInputFile

from config import Extensions, PROMPTS_DIR, IMAGES_DIR, MESSAGES_DIR, VOCAB_LANG


class Button:
    def __init__(self, name: str, callback: str | CallbackData):
        self.name = name
        self.callback = callback

    @classmethod
    def from_file(cls, file_name: str):
        path = PROMPTS_DIR / (file_name + Extensions.TXT.value)
        with open(path, 'r', encoding='UTF-8') as txt_file:
            name_line = txt_file.readline()
            name = name_line.split(', ')[0][5:]
        return cls(name, file_name)


class Buttons:
    def __init__(self):
        self.buttons = self._read_buttons()

    @staticmethod
    def _read_buttons() -> list[Button]:
        buttons_list = [file for file in os.listdir(PROMPTS_DIR) if file.startswith('talk_')]
        buttons = [Button.from_file(file.split('.')[0]) for file in buttons_list]
        return buttons

    def __iter__(self):
        return self

    def __next__(self):
        while self.buttons:
            return self.buttons.pop(0)
        raise StopIteration


class Resource:

    def __init__(self, file_name: str):
        self._file_name = file_name

    @property
    def photo(self):
        photo_path = IMAGES_DIR / (self._file_name + Extensions.JPG.value)
        if os.path.exists(photo_path):
            return FSInputFile(photo_path)

    @property
    def text(self):
        text_path = MESSAGES_DIR / (self._file_name + Extensions.TXT.value)
        if os.path.exists(text_path):
            with open(text_path, 'r', encoding='UTF-8') as file:
                return file.read()

    def as_kwargs(self) -> dict[str, FSInputFile | str]:
        return {'photo': self.photo, 'caption': self.text}


@dataclass
class TrainingWords:
    word: str
    word_translate: str
    lang_id: int

    @property
    def lang(self):
        return VOCAB_LANG[self.lang_id].language

    @property
    def flag(self):
        return VOCAB_LANG[self.lang_id].flag
