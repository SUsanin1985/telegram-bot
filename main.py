user_states = {}

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
import asyncio
import pytz
import logging
import json
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = "8114853660:AAGBlW7upsn8peFUnHYaiZw54-oe3b6AYWw"
ADMIN_ID = 7595922840

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📚 Курс для самостоятельного изучения", callback_data="menu_course")],
    [InlineKeyboardButton(text="👥 Обучение на мастера нового времени", callback_data="menu_group")],
    [InlineKeyboardButton(text="🧘‍♀️ Личная консультация", callback_data="menu_consult")],
    [InlineKeyboardButton(text="🌌 Индивидуальный ченнелинг", callback_data="menu_channeling")],
    [InlineKeyboardButton(text="💳 Вопросы по оплате", callback_data="menu_payments")],
    [InlineKeyboardButton(text="❓ Задать вопрос Алене", callback_data="ask_alena")],
    [],
    [InlineKeyboardButton(text="✨ Подписаться на соцсети", callback_data="menu_socials")],
])

TIME_SLOTS = {
    "Понедельник": ["11:00", "18:00"],
    "Среда": ["14:00", "19:00"],
    "Суббота": ["12:00"]
}

COMMON_TIMEZONES = [
    "Europe/Moscow", "Europe/Kiev", "Europe/Berlin",
    "Asia/Dubai", "Asia/Almaty", "Asia/Tokyo",
    "America/New_York", "America/Los_Angeles"
]

user_timezones = {}
consultation_map = {
    "consult_one_done": {
        "name": "Разовая консультация",
        "url": "https://estereon.getcourse.ru/sales/shop/dealPay/id/693220562/hash/804e"
    },
    "consult_three_done": {
        "name": "Пакет '3 шага'",
        "url": "https://estereon.getcourse.ru/sales/shop/dealPay/id/693222732/hash/6023"
    },
    "consult_four_done": {
        "name": "Углублённый маршрут",
        "url": "https://estereon.getcourse.ru/sales/shop/dealPay/id/693223401/hash/7426"
    }
}

pending_questions = set()

# --- Приветствие при /start ---
@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "<b>Добро пожаловать на портал Мастеров нового времени!</b>\n\n"
        "<i>Авторская система Алены Исмаиловой.</i>\n\n"
        "На стыке <b>телесной биологии</b>, <b>квантовой психологии</b> и <b>поля души</b>.\n"
        "<b>Открой свое предназначение</b> — и начни передавать его другим.\n\n"
        "🌐 <a href='https://estereonalena369.tilda.ws/'>Главная страница проекта</a>\n\n"
        "Я ваш виртуальный помощник.\n"
        "Выберите интересующий вас вопрос:",
        reply_markup=main_kb,
        disable_web_page_preview=True
    )

@dp.message(F.text)
async def handle_text(message: Message):
    if message.from_user.id in pending_questions:
        full_name = message.from_user.full_name
        username = message.from_user.username or "без username"
        text = "📩 Вопрос от <b>" + full_name + "</b> (@" + username + "):\n\n" + message.text
        await bot.send_message(ADMIN_ID, text, parse_mode="HTML")
        await message.answer("✅ Ваш вопрос отправлен Алене. Спасибо!")
        pending_questions.discard(message.from_user.id)
        return
    await message.answer("Привет! Выбери нужный раздел:", reply_markup=main_kb)

@dp.callback_query(F.data == "menu_start")
async def menu_back(callback: CallbackQuery):
    await callback.message.edit_text("Выберите, что вас интересует:", reply_markup=main_kb)

@dp.callback_query(F.data == "ask_alena")
async def ask_alena(callback: CallbackQuery):
    pending_questions.add(callback.from_user.id)
    await callback.message.answer("✍️ Напиши свой вопрос — просто следующим сообщением. Я передам его Алене.")

# --- Курс для самостоятельного изучения ---
@dp.callback_query(F.data == "menu_course")
async def course_self(callback: CallbackQuery):
    await callback.message.edit_text(
        "Курс сейчас находится в работе. Следите за новостями!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu_start")]]
        )
    )

# --- Обучение на мастера нового времени ---
@dp.callback_query(F.data == "menu_group")
async def group_menu(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Посвящение", callback_data="group_posv")],
        [InlineKeyboardButton(text="🌟 Мастер", callback_data="group_master")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_start")]
    ])
    await callback.message.edit_text("Выбери формат обучения:", reply_markup=kb)

@dp.callback_query(F.data == "group_posv")
async def group_posv(callback: CallbackQuery):
    text = (
        "🔥 <b>Формат: Посвящение</b>\n\n"
        "Авторская программа для тех, кто готов к личной трансформации и глубокому обновлению своей жизни. "
        "Ты получаешь практики, знания и опыт — и проходишь посвящение, которое меняет не только подход к себе, но и качество жизни.\n\n"
        "Что тебя ждет:\n"
        "• Погружение в методику Алены Исмайловой\n"
        "• Индивидуальные и групповые практики\n"
        "• Телесные, дыхательные, голосовые техники\n"
        "• Честное исследование себя и поддержка единомышленников\n"
        "• Мягкая, но мощная перезагрузка\n\n"
        "Длительность: 2 месяца (онлайн)\n"
        "После прохождения — <b>сертификат</b>.\n"
        "<b>Стоимость обучения — 150 000 ₽</b>.\n"
        "Старт ближайшего потока и стоимость — на сайте.\n\n"
        "🔗 <a href=\"https://estereonalena369.tilda.ws/portal\">Подробнее о Посвящении</a>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌟 Мастер", callback_data="group_master")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_group")]
    ])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

@dp.callback_query(F.data == "group_master")
async def group_master(callback: CallbackQuery):
    text = (
        "🌟 <b>Формат: Мастер</b>\n\n"
        "Профессиональное обучение для тех, кто хочет вести других — работать с людьми как практик новой школы.\n\n"
        "Что ты получишь:\n"
        "• Пошаговую систему работы с запросами клиента\n"
        "• Практики для развития интуиции и внимательности\n"
        "• Навыки ведения индивидуальных и групповых сессий\n"
        "• Возможность интегрировать квантовую телесную работу в любую помогающую профессию\n"
        "• <b>Диплом о профессиональной переподготовке государственного образца</b>\n"
        "• Сертификацию и поддержку после обучения\n\n"
        "Длительность: 3 месяца (онлайн + офлайн-интенсив)\n"
        "<b>Стоимость обучения — 200 000 ₽</b>.\n"
        "Подробная программа, старт потока и стоимость — на сайте.\n\n"
        "🔗 <a href=\"https://estereonalena369.tilda.ws/portal\">Подробнее о Мастере</a>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Посвящение", callback_data="group_posv")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_group")]
    ])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

# --- Индивидуальный ченнелинг ---
@dp.callback_query(F.data == "menu_channeling")
async def menu_channeling(callback: CallbackQuery):
    text = (
        "✨ <b>Индивидуальный ченнелинг</b>\n\n"
        "Это не «гадание», не «прогноз» и не «совет».\n"
        "Это — <b>вибрационная настройка твоей судьбы на твою настоящую частоту</b>.\n"
        "Когда логика уже не помогает, а душа шепчет, но ты не слышишь — приходит время заглянуть внутрь.\n\n"
        "🌌 <b>Во время сессии</b>:\n"
        "— ты получаешь не ответы, а коды своей реальности,\n"
        "— узнаёшь, где ты сбился с пути,\n"
        "— и вспоминаешь, кто ты на самом деле.\n\n"
        "Ты почувствуешь телом: мурашками, слезами, ясностью.\n"
        "Уйдёт шум. Останется только ты и твой свет.\n\n"
        "📌 <b>Подходит, если</b>:\n"
        "— стоишь на пороге важного выбора\n"
        "— застрял(а) в родовом или кармическом повторе\n"
        "— хочешь выйти из ловушки ума и начать доверять себе\n\n"
        "💫 Ощути этот сдвиг. Услышь свой внутренний голос.\n"
        "<b>Стоимость: 16 963 ₽</b>\n\n"
        "🔗 <a href='https://estereonalena369.tilda.ws/channeling'>Записаться на индивидуальный ченнелинг</a>"
    )
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu_start")]]
        )
    )

# --- Вопросы по оплате ---
@dp.callback_query(F.data == "menu_payments")
async def menu_payments(callback: CallbackQuery):
    text = (
        "💳 <b>Вопросы по оплате</b>\n\n"
        "Если у вас возник вопрос по оплате обучения или консультаций — просто напишите его сюда в чат. "
        "Мы ответим вам лично и поможем подобрать удобный способ оплаты!"
    )
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu_start")]]
        )
    )

# --- Соцсети ---
@dp.callback_query(F.data == "menu_socials")
async def menu_socials(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="YouTube: AlenaEstereon369 🎥", url="https://www.youtube.com/@AlenaEstereon369")],
        [InlineKeyboardButton(text="YouTube: Квантовое исцеление 🌀", url="https://www.youtube.com/@EstereonAlena369")],
        [InlineKeyboardButton(text="Instagram 📸", url="https://www.instagram.com/esterionalena369")],
        [InlineKeyboardButton(text="Telegram-канал ✈️", url="https://t.me/iscelenie_d")],
        [InlineKeyboardButton(text="Яндекс Дзен 📝", url="https://dzen.ru/id/66af4ff56d1ffe1951b33cb7")],
        [InlineKeyboardButton(text="RuTube ▶️", url="https://rutube.ru/channel/38300427/")],
        [InlineKeyboardButton(text="🔙 В меню", callback_data="menu_start")],
    ])
    await callback.message.edit_text(
        "<b>Подписывайтесь на соцсети и будьте в потоке новостей, трансляций и вдохновения:</b>",
        parse_mode="HTML",
        reply_markup=kb
    )

# --- Консультации ---
@dp.callback_query(F.data == "menu_consult")
async def personal_consult(callback: CallbackQuery):
    consult_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Разовая консультация", callback_data="consult_one")],
        [InlineKeyboardButton(text="🟡 Пакет '3 шага'", callback_data="consult_three")],
        [InlineKeyboardButton(text="🔵 Углублённый маршрут", callback_data="consult_four")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu_start")]
    ])
    await callback.message.edit_text("🧘 <b>Личная консультация</b>\n\nВыбери формат консультации, чтобы увидеть подробности:", reply_markup=consult_kb)

@dp.callback_query(F.data == "consult_one")
async def consult_one(callback: CallbackQuery):
    text = (
        "<b>✨ Разовая консультация</b>\n\n"
        "Индивидуальная сессия для прояснения ситуации и выхода из тупика.\n\n"
        "⏳ <b>Длительность:</b> 60–90 мин (Zoom/Telegram)\n"
        "💳 <b>Стоимость:</b> 12 369 ₽\n\n"
        "<a href='https://estereon.getcourse.ru/consultation'>✨ Подробнее и записаться</a>"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu_consult")]]
    ))

@dp.callback_query(F.data == "consult_three")
async def consult_three(callback: CallbackQuery):
    text = (
        "<b>✨ Пакет «3 шага»</b>\n\n"
        "Пошаговая работа с поддержкой и внедрением изменений в жизнь.\n\n"
        "⏳ <b>Длительность:</b> 3 сессии с поддержкой между встречами\n"
        "💳 <b>Стоимость:</b> 33 369 ₽\n\n"
        "<a href='https://estereon.getcourse.ru/threestep'>✨ Подробнее и записаться</a>"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu_consult")]]
    ))

@dp.callback_query(F.data == "consult_four")
async def consult_four(callback: CallbackQuery):
    text = (
        "<b>✨ Углублённый маршрут (4 сессии + сопровождение)</b>\n\n"
        "Глубокая работа по полной перезагрузке восприятия и жизненных сценариев.\n\n"
        "⏳ <b>Длительность:</b> 4 сессии + сопровождение в Telegram\n"
        "💳 <b>Стоимость:</b> 44 369 ₽\n\n"
        "<a href='https://estereon.getcourse.ru/fourstep'>✨ Подробнее и записаться</a>"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu_consult")]]
    ))

async def main():
    logging.basicConfig(level=logging.INFO)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
