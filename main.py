import logging
import os
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, ParseMode)
from asyncpg import InterfaceError
from sqlalchemy.exc import SQLAlchemyError

from database.database_manager import fetch_dates, get_horoscope_data, save_user
from keyboards import inline_kb_full, inline_kb_menu
from models.models import HoroscopeData, LoveHoroscopeData, FinanceHoroscopeData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot_token = os.environ.get('BOT_TOKEN')
port = os.environ.get('PORT')

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())



@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username

    await save_user(user_id, username)
    logger.info(f"User {username} ({user_id}) started the bot.")  # Log user start

    await bot.send_sticker(user_id, sticker="CAACAgIAAxkBAAEJ1Z1kw08f2y6zz4A7rheTsOh_npqF7gACVB0AAoqR0ElUTMG-FBDOOy8E")
    await message.reply(
        "Добро пожаловать в гороскоп бот!\n"
        "Пожалуйста выберите тип предсказания:",
        reply_markup=inline_kb_menu
    )
    await state.set_state('menu_option')


@dp.callback_query_handler(lambda c: c.data.startswith('меню_'), state='menu_option')
async def process_menu(callback_query: CallbackQuery, state: FSMContext):
    selected_menu_option = callback_query.data.split('_')[1]
    await state.update_data(selected_menu_option=selected_menu_option)
    chat_id = callback_query.from_user.id

    logger.info(f"User {chat_id} selected menu option: {selected_menu_option}")  # Log menu selection

    await bot.send_message(
        chat_id=chat_id,
        text="Выберите ваш знак зодиака:",
        reply_markup=inline_kb_full
    )
    await state.set_state('zodiac_sign')
    await callback_query.answer()


@dp.message_handler(state='*')
async def handle_unexpected_messages(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if await state.get_state() is not None:
        await message.reply("Пожалуйста, используйте кнопки для взаимодействия с ботом.")
    else:
        await message.reply("Неизвестная команда. Для начала работы с ботом используйте /start.")
        logger.warning(f"User {message.from_user.id} sent an unexpected message: {message.text}")  # Log unexpected messages


@dp.callback_query_handler(lambda c: c.data.startswith('знак_'), state='zodiac_sign')
async def process_zodiac_sign(callback_query: CallbackQuery, state: FSMContext):
    zodiac_sign = callback_query.data.split('_')[1]
    await state.update_data(zodiac_sign=zodiac_sign)
    chat_id = callback_query.from_user.id

    logger.info(f"User {chat_id} selected zodiac sign: {zodiac_sign}")  # Log zodiac sign selection

    dates = await fetch_dates(zodiac_sign, HoroscopeData)

    await show_date_keyboard(chat_id, dates)
    await state.set_state('day_of_week')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data.startswith('дата_'), state='day_of_week')
async def day_of_week(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    zodiac_sign = user_data.get('zodiac_sign')
    selected_menu_option = user_data.get('selected_menu_option')
    date = callback_query.data.split('_')[1]
    chat_id = callback_query.from_user.id

    try:
        if selected_menu_option == 'Гороскоп':
            horoscope_data = await get_horoscope_data(date, zodiac_sign, HoroscopeData)
            await bot.send_sticker(chat_id,
                                   sticker="CAACAgIAAxkBAAEJ1blkw0-Hhn-qhFZi2qFQtK37LVoNKwACQxEAAogjeUm7XAjLk6X4TS8E")
        elif selected_menu_option == 'Любовный':
            horoscope_data = await get_horoscope_data(date, zodiac_sign, LoveHoroscopeData)
            await bot.send_sticker(chat_id,
                                   sticker="CAACAgIAAxkBAAEJ1Y5kw0veMxR325K6NR5TFFOjXDFmRgAC1xkAAmIGcEmfFezVajtprS8E")
        elif selected_menu_option == 'Финансовый':
            horoscope_data = await get_horoscope_data(date, zodiac_sign, FinanceHoroscopeData)
            await bot.send_sticker(chat_id,
                                   sticker="CAACAgIAAxkBAAEJ1a9kw09jGIFoIKoAAcvqOU6_fd_dk6QAAo4ZAAJyUThJlnmGIsWVVecvBA")
        else:
            horoscope_data = None

        if horoscope_data:
            horoscope_text = horoscope_data.text
            message = f"Предсказание на {date} для знака {zodiac_sign}:\n\n{horoscope_text}"
            await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)

            await show_another_day_keyboard(chat_id)
            await dp.current_state().set_state('another_day_option')
            logger.info(f"Sent horoscope for {zodiac_sign} on {date} to user {chat_id}.")  # Log horoscope sent

    except (InterfaceError, SQLAlchemyError) as e:
        await bot.send_message(chat_id=chat_id, text="Ошибка соединения с базой данных. Пожалуйста, попробуйте позже.")
        logger.exception("An error occurred while querying the database.")  # Log exception details
        await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith('ответ_'), state='another_day_option')
async def another_day_option(callback_query: CallbackQuery, state: FSMContext):
    answer = callback_query.data.split('_')[1]
    chat_id = callback_query.from_user.id

    logger.info(f"User {chat_id} selected another day option: {answer}")  # Log user response to options

    if answer == 'да':
        user_data = await state.get_data()
        zodiac_sign = user_data.get('zodiac_sign')

        dates = await fetch_dates(zodiac_sign, HoroscopeData)

        await show_date_keyboard(chat_id, dates)
        await dp.current_state().set_state('day_of_week')

    elif answer == 'знак':
        await bot.send_message(
            chat_id=chat_id,
            text="Пожалуйста, выберите знак зодиака для получения новых предсказаний:",
            reply_markup=inline_kb_full
        )
        await dp.current_state().set_state('zodiac_sign')

    elif answer == 'категория':
        await bot.send_message(
            chat_id=chat_id,
            text="Добро пожаловать в гороскоп бот!\n"
            "Пожалуйста выберите тип предсказания:",
            reply_markup=inline_kb_menu
        )
        await state.set_state('menu_option')

    elif answer == 'нет':
        await bot.send_message(chat_id=chat_id,
                               text="Используйте полученные знания разумно!\n\n"
                                    "Для повторного общения с ботом нажмите на ссылку: /start")
        await bot.send_sticker(chat_id=chat_id,
                               sticker="CAACAgIAAxkBAAEJ1ZVkw08EVSkElV3HWH-uDC9dCYbPzQAC9BQAAgUGeEk53VXKRWEqWy8E")

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
    keyboard.add(InlineKeyboardButton("Да", callback_data="ответ_да")) \
        .add(InlineKeyboardButton("Нет", callback_data="ответ_нет")) \
        .add(InlineKeyboardButton("Выбрать новый знак", callback_data="ответ_знак")) \
        .add(InlineKeyboardButton("Выбрать новую категорию", callback_data="ответ_категория"))

    await bot.send_message(
        chat_id=chat_id,
        text="Хотите получить предсказание на другой день?",
        reply_markup=keyboard
    )


if __name__ == '__main__':
    logger.info("Bot started...")
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True)