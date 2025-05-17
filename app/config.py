import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GPT_TOKEN = os.getenv('GPT_TOKEN')
PROXY = os.getenv('PROXY')
MAX_CAPTION_LENGTH = 1024

BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = BASE_DIR / 'resources'
PROMPTS_DIR = RESOURCES_DIR / 'prompts'
IMAGES_DIR = RESOURCES_DIR / 'images'
MESSAGES_DIR = RESOURCES_DIR / 'messages'


class Extensions(Enum):
    JPG = '.jpg'
    TXT = '.txt'


class GPTRole(Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


class FSMKey(Enum):
    COUNTER_SUCCESS = 'counter_success'
    COUNTER_TOTAL = 'counter_total'

    TRAINING_WORDS = 'training_words'
    TRAINING_CURRENT = 'training_current'
    VOCAB_MESSAGE_ID = 'vocab_message_id'
    TRANSLATOR = 'translator'


class GPTModel(str, Enum):
    GPT4o = "gpt-4o"
    GPT4_TURBO = "gpt-4-turbo"
    GPT3_5_TURBO = "gpt-3.5-turbo"

    @classmethod
    def default(cls) -> 'GPTModel':
        return cls.GPT3_5_TURBO


@dataclass
class ButtonConfig:
    flag: str
    language: str


LANGS = [
    ButtonConfig("🇬🇧", "Английский"),
    ButtonConfig("🇩🇪", "Немецкий"),
    ButtonConfig("🇪🇸", "Испанский"),
    ButtonConfig("🇫🇷", "Французский"),
]
