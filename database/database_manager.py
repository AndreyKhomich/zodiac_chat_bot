import uuid

from sqlalchemy.exc import SQLAlchemyError

from models.models import ZodiacSign, User

from sqlalchemy import insert, select, delete
from database.database import async_session_maker
from parser.scraper import get_horoscope


async def fetch_dates(zodiac_sign, horoscope_model):
    async with async_session_maker() as session:
        query = (
            select(horoscope_model.c.date)
            .select_from(horoscope_model.join(ZodiacSign, horoscope_model.c.zodiac_sign_id == ZodiacSign.c.id))
            .where(ZodiacSign.c.name == zodiac_sign)
            .distinct()
        )
        try:
            result = await session.execute(query)
            dates = [row[0] for row in result.fetchall()][-7:]
            return dates
        except SQLAlchemyError as e:
            raise e


async def get_horoscope_data(date, zodiac_sign, horoscope_model):
    async with async_session_maker() as session:
        query = (
            select(horoscope_model)
            .select_from(horoscope_model.join(ZodiacSign, horoscope_model.c.zodiac_sign_id == ZodiacSign.c.id))
            .where(horoscope_model.c.date == date)
            .where(ZodiacSign.c.name == zodiac_sign)
        )
        try:
            result = await session.execute(query)
            horoscope_data = result.fetchone()
            return horoscope_data
        except SQLAlchemyError as e:
            raise e


async def delete_all_horoscopes(horoscope_model):
    async with async_session_maker() as session:
        delete_statement = delete(horoscope_model)
        await session.execute(delete_statement)
        await session.commit()


async def scrape_and_save_horoscope_data(horoscope_model, horoscope):
    async with async_session_maker() as session:
        for horoscope in horoscope:
            url = horoscope['url']
            zodiac_sign_id = horoscope['zodiac_sign_id']
            horoscope_data = get_horoscope(url, zodiac_sign_id)

            for data in horoscope_data:
                data['id'] = str(uuid.uuid4())
                date = data['date']
                data['zodiac_sign_id'] = zodiac_sign_id

                insert_statement = insert(horoscope_model).values(**data)
                await session.execute(insert_statement)

            await session.commit()


async def save_user(user_id, username):
    async with async_session_maker() as session:
        try:
            existing_user = await session.execute(select(User).where(User.columns.id == user_id))
            if existing_user.fetchone() is None:
                insert_statement = insert(User).values(id=user_id, username=username)
                await session.execute(insert_statement)
                await session.commit()
        except Exception as e:
            print("Error saving user menu interaction:", e)
