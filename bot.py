import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from config import BOT_TOKEN, LOGO_URL, CHANNEL_ID
from keyboards import (
    language_keyboard,
    start_keyboard_ru,
    start_keyboard_uz,
    back_keyboard
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_data = {}

# Вопросы по языкам
questions = {
    "ru": [
        ("title", "Введите *название вакансии*:"),
        ("location", "📍 Укажите *локацию*:"),
        ("salary", "💰 Укажите *зарплату*:"),
        ("experience", "💼 Укажите *опыт работы*:"),
        ("contact", "📱 Укажите *контакты* (номер или Telegram):"),
        ("requirements", "📌 Опишите *требования*:"),
        ("description", "📝 Опишите *обязанности*:"),
        ("time", "🕰️ Укажите *время работы*:"),
        ("days", "📅 Укажите *дни работы*:")
    ],
    "uz": [
        ("title", "Vakansiya *nomini kiriting*:"),
        ("location", "📍 *Joylashuvni* kiriting:"),
        ("salary", "💰 *Maoshni* kiriting:"),
        ("experience", "💼 *Tajriba darajasini* kiriting:"),
        ("contact", "📱 *Aloqa uchun* raqam yoki Telegram:"),
        ("requirements", "📌 *Talablar* haqida yozing:"),
        ("description", "📝 *Vazifalar* haqida yozing:"),
        ("time", "🕰️ *Ish vaqtini* kiriting:"),
        ("days", "📅 *Ish kunlari*ni kiriting:")
    ]
}

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("🌐 Выберите язык / Tilni tanlang:", reply_markup=language_keyboard)

@dp.message(F.text.in_(["🇷🇺 Русский", "🇺🇿 O‘zbek"]))
async def language_choice(message: Message):
    lang = "ru" if "Рус" in message.text else "uz"
    user_data[message.from_user.id] = {"lang": lang, "data": {}}

    keyboard = start_keyboard_ru if lang == "ru" else start_keyboard_uz
    btn = "📝 Добавить вакансию" if lang == "ru" else "📝 Vakansiya qo‘shish"

    await message.answer(f"{message.text} выбран ✅\nНажмите кнопку «{btn}»", reply_markup=keyboard)

@dp.message(F.text.in_(["📝 Добавить вакансию", "📝 Vakansiya qo‘shish"]))
async def start_vacancy(message: Message):
    user = user_data.get(message.from_user.id, {})
    if not user:
        await message.answer("Сначала выберите язык.")
        return

    user["data"] = {}
    qlist = questions[user["lang"]]
    await message.answer(qlist[0][1], parse_mode="Markdown", reply_markup=back_keyboard)

@dp.message()
async def handle_input(message: Message):
    user = user_data.get(message.from_user.id)
    if not user:
        await message.answer("Сначала выберите язык.")
        return

    lang = user["lang"]
    data = user["data"]
    step = len(data)
    qlist = questions[lang]

    # Обработка "Назад"
    if message.text == "🔙 Назад":
        if step == 0:
            await message.answer("🚫 Назад нельзя. Вы на первом шаге.")
            return
        removed_key = list(data.keys())[-1]
        data.pop(removed_key)
        prev_step = len(data)
        await message.answer(f"🔄 Повторите ввод:\n\n{qlist[prev_step][1]}", parse_mode="Markdown", reply_markup=back_keyboard)
        return

    if step < len(qlist):
        key, _ = qlist[step]
        data[key] = message.text

        if step + 1 < len(qlist):
            await message.answer(qlist[step + 1][1], parse_mode="Markdown", reply_markup=back_keyboard)
        else:
            await send_post_dual_language(data)
            keyboard = start_keyboard_ru if lang == "ru" else start_keyboard_uz
            await message.answer("✅ Вакансия отправлена в канал.", reply_markup=keyboard)
            user["data"] = {}

# Публикация на двух языках
async def send_post_dual_language(data):
    ru_text = (
        f"📢 *{data['title']}*\n"
        f"📍 Локация: {data['location']}\n"
        f"💰 Зарплата: {data['salary']}\n"
        f"💼 Опыт: {data['experience']}\n"
        f"📱 Контакты: {data['contact']}\n"
        f"📌 Требования: {data['requirements']}\n"
        f"📝 Обязанности: {data['description']}\n"
        f"🕰️ Время работы: {data['time']}\n"
        f"📅 Дни работы: {data['days']}"
    )

    uz_text = (
        f"📢 *{data['title']}*\n"
        f"📍 Joylashuv: {data['location']}\n"
        f"💰 Maosh: {data['salary']}\n"
        f"💼 Tajriba: {data['experience']}\n"
        f"📱 Aloqa: {data['contact']}\n"
        f"📌 Talablar: {data['requirements']}\n"
        f"📝 Vazifalar: {data['description']}\n"
        f"🕰️ Ish vaqti: {data['time']}\n"
        f"📅 Ish kunlari: {data['days']}"
    )

    caption = f"📄 *Вакансия / Vakansiya*\n\n🇷🇺\n{ru_text}\n\n🇺🇿\n{uz_text}"

    await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=LOGO_URL,
        caption=caption,
        parse_mode="Markdown"
    )

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
