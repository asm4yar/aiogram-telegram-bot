from aiogram.fsm.state import State, StatesGroup


class ChatGPTRequests(StatesGroup):
    wait_for_request = State()


class CelebrityTalk(StatesGroup):
    wait_for_answer = State()


class Quiz(StatesGroup):
    wait_for_answer = State()
    wait_for_next_action = State()

class Vocab(StatesGroup):
    words = State()
    message_training = State()
