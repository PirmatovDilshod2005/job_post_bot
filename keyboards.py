from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Выбор языка
language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O‘zbek")],
    ],
    resize_keyboard=True
)

# Главные меню
start_keyboard_ru = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📝 Добавить вакансию")]],
    resize_keyboard=True
)

start_keyboard_uz = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📝 Vakansiya qo‘shish")]],
    resize_keyboard=True
)

# Кнопка "Назад"
back_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔙 Назад")]],
    resize_keyboard=True,
    one_time_keyboard=True
)
