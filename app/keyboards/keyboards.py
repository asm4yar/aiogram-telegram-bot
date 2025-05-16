from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_reply(buttons):
    keyboard = ReplyKeyboardBuilder()
    for button in buttons:
        keyboard.button(
            text=button,
        )
    return keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню...',
    )


def kb_end_talk():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='Попрощаться!',
    )
    return keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Задайте свой вопрос...',
        one_time_keyboard=True,
    )
