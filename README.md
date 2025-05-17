
Telegram-бот с подключением ChatGPT
Реализованы функциональности:
/start - главное меню бота
/random - узнать рандомный факт · 🧠
/gpt - Задать вопрос ChatGPT · 🤖
/talk - поговорить с известной личностью · 👤
/quiz - проверить свои знания ❓
/vocab - Словарный тренажёр 📚
/translator - Переводчик 📚

```text

Для запуска бота создать файл .env в каталоге app
Добавить в файл .env переменные окружения
BOT_TOKEN - токен бота
GPT_TOKEN - токен - ChatGPT
PROXY(опционально) - прокси, поддерживается socks5, указать в формате URI например socks5://127.0.0.1:1080

Схема проекта:

├── app
│   ├── classes
│   │   ├── chat_gpt.py
│   │   ├── __init__.py
│   │   └── resource.py
│   ├── config.py
│   ├── .env
│   ├── handlers
│   │   ├── callback_handlers.py
│   │   ├── command.py
│   │   ├── error_handlers.py
│   │   ├── handlers.py
│   │   ├── handlers_state.py
│   │   ├── __init__.py
│   │   └── message_handler.py
│   ├── keyboards
│   │   ├── callback_data.py
│   │   ├── __init__.py
│   │   ├── inline_keyboards.py
│   │   └── keyboards.py
│   ├── main.py
│   ├── misc.py
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── README.md
└── resources
    ├── images
    │   ├── avatar_main.jpg
    │   ├── gpt.jpg
    │   ├── main.jpg
    │   ├── message.jpg
    │   ├── quiz.jpg
    │   ├── random.jpg
    │   ├── talk_cobain.jpg
    │   ├── talk_hawking.jpg
    │   ├── talk.jpg
    │   ├── talk_nietzsche.jpg
    │   ├── talk_queen.jpg
    │   ├── talk_tolkien.jpg
    │   ├── translator.jpg
    │   └── vocab.jpg
    ├── messages
    │   ├── gpt.txt
    │   ├── main.txt
    │   ├── quiz.txt
    │   ├── random.txt
    │   ├── talk.txt
    │   ├── translator_lang_select.txt
    │   ├── translator.txt
    │   └── vocab.txt
    └── prompts
        ├── gpt.txt
        ├── main.txt
        ├── quiz.txt
        ├── random.txt
        ├── talk_cobain.txt
        ├── talk_hawking.txt
        ├── talk_nietzsche.txt
        ├── talk_queen.txt
        ├── talk_tolkien.txt
        ├── translator.txt
        ├── vocab_training.txt
        └── vocab.txt

9 directories, 56 files
```
