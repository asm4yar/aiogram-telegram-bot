from typing import List, Dict
from typing import Callable
import httpx
import openai

from config import GPT_TOKEN, PROXY, PROMPTS_DIR, Extensions, GPTRole, GPTModel

MessageType = List[Dict[str, str]]


class GPTMessage:

    def __init__(self, prompt: str, func: Callable[[str], str] = lambda x: x):
        self.func = func
        self.prompt_file = PROMPTS_DIR / (prompt + Extensions.TXT.value)
        self.message_list: MessageType = self._init_message()

    def _init_message(self) -> list[dict[str, str]]:
        message = {
            'role': GPTRole.SYSTEM.value,
            'content': self._load_prompt(),
        }
        return [message]

    def _load_prompt(self) -> str:
        with open(self.prompt_file, 'r', encoding='UTF-8') as file:
            prompt = self.func(file.read())
        return prompt

    def update(self, role: GPTRole, message: str):
        message = {
            'role': role.value,
            'content': message,
        }
        self.message_list.append(message)


class ChatGPT:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def _normalize_gpt_token(token: str):
        return 'sk-proj-' + token[:3:-1] if token.startswith('gpt:') else token

    def __init__(self, model: str = GPTModel.default()):
        self._gpt_token = ChatGPT._normalize_gpt_token(GPT_TOKEN)
        self._proxy = PROXY
        self._client = self._create_client()
        self._model = model

    def _create_client(self):
        return openai.AsyncOpenAI(
            api_key=self._gpt_token,
            http_client=httpx.AsyncClient(
                proxy=self._proxy,
                verify=False
            )
        )

    async def request(self, messages: GPTMessage) -> str:
        response = await self._client.chat.completions.create(
            messages=messages.message_list,
            model=self._model,
        )
        return response.choices[0].message.content
