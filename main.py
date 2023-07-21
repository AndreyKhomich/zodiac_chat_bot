import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, ParseMode, ReplyKeyboardMarkup)
from asyncpg import InterfaceError
from sqlalchemy.exc import SQLAlchemyError

from database.database_manager import DatabaseManager
from utils.keyboards import inline_kb_full

month_mapping = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12
}

bot_token = os.environ.get('BOT_TOKEN')
port = os.environ.get('PORT')

# Create the bot and dispatcher
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await message.reply(
        "Добро пожаловать в гороскоп бот!\n"
        "Для получения предсказания, пожалуйста выберите ваш знак зодиака:",
        reply_markup=inline_kb_full
    )
    await state.set_state('zodiac_sign')


@dp.message_handler(commands=['start'], state='*')
async def handle_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if await state.get_state() is not None:
        await message.reply("Вы уже начали общение с ботом. Пожалуйста используйте кнопки для взаимодействия.")
    else:
        await start(message)


@dp.message_handler(state='*')
async def handle_unexpected_messages(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if await state.get_state() is not None:
        await message.reply("Пожалуйста, используйте кнопки для взаимодействия с ботом.")
    else:
        await message.reply("Неизвестная команда. Для начала работы с ботом используйте /start.")


@dp.callback_query_handler(lambda c: c.data.startswith('знак_'), state='zodiac_sign')
async def process_zodiac_sign(callback_query: CallbackQuery, state: FSMContext):
    zodiac_sign = callback_query.data.split('_')[1]
    await state.update_data(zodiac_sign=zodiac_sign)
    chat_id = callback_query.from_user.id

    database_manager = DatabaseManager()
    dates = await database_manager.fetch_dates(zodiac_sign)

    await show_date_keyboard(chat_id, dates)
    await state.set_state('day_of_week')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data.startswith('дата_'), state='day_of_week')
async def day_of_week(callback_query: CallbackQuery, state: FSMContext):
    date = callback_query.data.split('_')[1]
    chat_id = callback_query.from_user.id

    try:
        user_data = await state.get_data()
        zodiac_sign = user_data.get('zodiac_sign')

        database_manager = DatabaseManager()
        horoscope_data = await database_manager.get_horoscope_data(date, zodiac_sign)

        if horoscope_data:
            horoscope_text = horoscope_data.text
            message = f"Предсказание на {date} для знака {zodiac_sign}:\n\n{horoscope_text}"
            await bot.send_message(chat_id=chat_id,
                                   text=message,
                                   parse_mode=ParseMode.MARKDOWN)

            await show_another_day_keyboard(chat_id)
            await dp.current_state().set_state('another_day_option')

    except (InterfaceError, SQLAlchemyError):
        await bot.send_message(chat_id=chat_id,
                               text="Ошибка соединения с базой данных. Пожалуйста, попробуйте позже."
                               )
        logging.exception("An error occurred while querying the database.")
        await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith('ответ_'), state='another_day_option')
async def another_day_option(callback_query: CallbackQuery, state: FSMContext):
    answer = callback_query.data.split('_')[1]
    chat_id = callback_query.from_user.id

    if answer == 'да':
        user_data = await state.get_data()
        zodiac_sign = user_data.get('zodiac_sign')

        database_manager = DatabaseManager()
        dates = await database_manager.fetch_dates(zodiac_sign)

        await show_date_keyboard(chat_id, dates)
        await dp.current_state().set_state('day_of_week')

    elif answer == 'знак':
        await bot.send_message(
            chat_id=chat_id,
            text="Пожалуйста, выберите знак зодиака для получения новых предсказаний:",
            reply_markup=inline_kb_full
        )
        await dp.current_state().set_state('zodiac_sign')

    elif answer == 'нет':
        await bot.send_message(chat_id=chat_id,
                               text="Используйте полученные знания разумно!\n\n"
                                    "Для повторного общения с ботом нажмите на ссылку: /start")
        await state.finish()

    await callback_query.answer()


async def show_date_keyboard(chat_id, dates):
    keyboard = InlineKeyboardMarkup()

    for date in dates:
        button = InlineKeyboardButton(date, callback_data='дата_' + date)
        keyboard.insert(button)

    await bot.send_message(
        chat_id=chat_id,
        text="Выберите дату, для которой вы хотели бы получить предсказание:",
        reply_markup=keyboard
    )


async def show_another_day_keyboard(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Да", callback_data="ответ_да"))\
        .add(InlineKeyboardButton("Нет", callback_data="ответ_нет"))\
        .add(InlineKeyboardButton("Выбрать новый знак", callback_data="ответ_знак"))

    await bot.send_message(
        chat_id=chat_id,
        text="Вы желаете получить предсказание на другой день или выбрать новый знак зодиака?",
        reply_markup=keyboard
    )


async def run_bot(dispatcher: Dispatcher):
    await bot.set_webhook(url=f"https://zodiacbot.herokuapp.com/webhook/{bot_token}", drop_pending_updates=True)
    await bot.set_webhook(url=None)
    await dispatcher.start_polling()


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=f'/webhook/{bot_token}',
        on_startup=run_bot,
        skip_updates=True,
        host='0.0.0.0',
        port=port,
    )
