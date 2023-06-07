import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from sqlalchemy import select
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode

from database import async_session_maker
from models.models import HoroscopeData, ZodiacSign

bot_token = os.environ.get('BOT_TOKEN')

# Create the bot and dispatcher
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


# Asynchronous handler for the /start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Добро пожаловать в гороскоп бот!\n"
                        "Для получения предсказания, пожалуйста введите ваш знак зодиака:")
    await dp.current_state().set_state('zodiac_sign')


# Asynchronous handler for text messages
@dp.message_handler(state='zodiac_sign', content_types=types.ContentType.TEXT)
async def text_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    zodiac_sign = message.text

    # Save the user's zodiac sign in the context
    await state.update_data(zodiac_sign=zodiac_sign)

    # Ask for the day of the week
    await bot.send_message(chat_id=chat_id, text="Выберите дату на этой неделе, для которой вы хотели "
                                                 "бы получить предсказание:")

    # Update the state to 'day_of_week' after asking for zodiac sign
    await dp.current_state().set_state('day_of_week')


# Asynchronous handler for the day of the week selection
@dp.message_handler(state='day_of_week', content_types=types.ContentType.TEXT)
async def day_of_week(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    day_of_week = message.text

    # Retrieve the zodiac sign from the state
    user_data = await state.get_data()
    zodiac_sign = user_data.get('zodiac_sign')

    # Retrieve the corresponding horoscope data from the database
    async with async_session_maker() as session:
        query = (
            select(HoroscopeData)
            .select_from(HoroscopeData.join(ZodiacSign, HoroscopeData.c.zodiac_sign_id == ZodiacSign.c.id))
            .where(HoroscopeData.c.date == day_of_week)
            .where(ZodiacSign.c.name == zodiac_sign)
        )
        result = await session.execute(query)
        horoscope_data = result.fetchone()

    if horoscope_data:
        horoscope_text = horoscope_data.text
        await bot.send_message(chat_id=chat_id, text=horoscope_text, parse_mode=ParseMode.MARKDOWN)

        # Prompt the user to choose another day or finish the conversation
        await bot.send_message(chat_id=chat_id, text="Вы желаете получить предсказание на другой день? "
                                                     "Пожалуйста, введите 'да' или 'нет'.")
        await dp.current_state().set_state('another_day_option')
    else:
        await bot.send_message(chat_id=chat_id, text="Данные гороскопа для указанного знака зодиака "
                                                     "и дня недели не надены.")

        # Finish the conversation
        await state.finish()
        await session.close()


# Asynchronous handler for the another day option
@dp.message_handler(state='another_day_option', content_types=types.ContentType.TEXT)
async def another_day_option(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    option = message.text.lower()

    if option == 'да':
        await bot.send_message(chat_id=chat_id, text="Пожалуйста выберите другую дату на этой неделе:")
        await dp.current_state().set_state('day_of_week')
    elif option == 'нет':
        await bot.send_message(chat_id=chat_id, text="Используйте полученные знания разумно!")
        await state.finish()
    else:
        await bot.send_message(chat_id=chat_id, text="Не верный ответ. Пожалуйста введите 'да' или 'нет'.")


# Start the bot
async def run_bot():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(run_bot())
