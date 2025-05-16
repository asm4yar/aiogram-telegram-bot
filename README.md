Telegram-бот с подключением ChatGPT
Реализованы функциональности:
1. /start — главное меню бота
2. /random - узнать рандомный факт · 🧠
3. /gpt - Задать вопрос ChatGPT · 🤖
4. /talk - поговорить с известной личностью · 👤
5. /quiz - проверить свои знания ❓
6. /vocab - Словарный тренажёр 📚

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
├── readme.txt
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
    │   └── vocab.jpg
    ├── messages
    │   ├── gpt.txt
    │   ├── main.txt
    │   ├── quiz.txt
    │   ├── random.txt
    │   ├── talk.txt
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
        ├── vocab_training.txt
        └── vocab.txt

9 directories, 52 files
