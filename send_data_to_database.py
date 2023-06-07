import asyncio
import json
import os

from sqlalchemy import insert

from database import async_session_maker
from models.models import HoroscopeData

zodiacs_folder = "zodiacs_data"

# Load the JSON data from the "zodiac_signs.json" file
with open('zodiac_signs.json', 'r', encoding='utf-8') as zodiac_file:
    zodiac_signs_data = json.load(zodiac_file)


async def insert_horoscope_data():
    async with async_session_maker() as session:
        for zodiac_data in zodiac_signs_data:
            horoscope_file_path = os.path.join(zodiacs_folder, zodiac_data['name'], 'horoscope_data.json')
            with open(horoscope_file_path, 'r', encoding='utf-8') as horoscope_file:
                horoscope_data = json.load(horoscope_file)

            for horoscope in horoscope_data:
                insert_horoscope = insert(HoroscopeData).values(
                    id=horoscope['id'],
                    date=horoscope['date'],
                    text=horoscope['text'],
                    zodiac_sign_id=zodiac_data['id']
                )
                await session.execute(insert_horoscope)

        await session.commit()


async def main():
    await insert_horoscope_data()

asyncio.run(main())
