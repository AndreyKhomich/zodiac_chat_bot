from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session_maker
from models.models import HoroscopeData, ZodiacSign


class DatabaseManager:
    async def fetch_dates(self, zodiac_sign):
        async with async_session_maker() as session:
            query = (
                select(HoroscopeData.c.date)
                .select_from(HoroscopeData.join(ZodiacSign, HoroscopeData.c.zodiac_sign_id == ZodiacSign.c.id))
                .where(ZodiacSign.c.name == zodiac_sign)
                .distinct()
            )
            try:
                result = await session.execute(query)
                dates = [row[0] for row in result.fetchall()][-7:]
                return dates
            except SQLAlchemyError as e:
                raise e

    async def get_horoscope_data(self, date, zodiac_sign):
        async with async_session_maker() as session:
            query = (
                select(HoroscopeData)
                .select_from(HoroscopeData.join(ZodiacSign, HoroscopeData.c.zodiac_sign_id == ZodiacSign.c.id))
                .where(HoroscopeData.c.date == date)
                .where(ZodiacSign.c.name == zodiac_sign)
            )
            try:
                result = await session.execute(query)
                horoscope_data = result.fetchone()
                return horoscope_data
            except SQLAlchemyError as e:
                raise e
