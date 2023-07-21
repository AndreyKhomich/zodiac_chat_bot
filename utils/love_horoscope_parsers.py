import asyncio
import uuid

import requests
from bs4 import BeautifulSoup
from sqlalchemy import insert, select

from database.database import async_session_maker
from models.models import ManHoroscopeData

horoscopes = [
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/skorpion-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 638
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/vesy-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 635
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/strelets-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 408
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/kozerog-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 81
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/vodolej-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 433
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/ryby-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 310
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/oven-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 449
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/telets-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 571
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/bliznetsy-lyubovnyj-nedelya.htmll',
        'zodiac_sign_id': 727
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/rak-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 288
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/lev-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 978
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/deva-lyubovnyj-nedelya.html',
        'zodiac_sign_id': 664
    },
]

Session = async_session_maker()


def get_horoscope(url, zodiac_sign_id):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }

    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    src = r.text

    soup = BeautifulSoup(src, "html.parser")
    date_elements = soup.find_all('i', class_='sprl')

    horoscope_data = []
    for date_element in date_elements:
        date = date_element.text.strip().split(' ')[-2:]
        date = ' '.join(date)
        text = date_element.find_next_sibling('div').text.strip()
        entry = {'date': date, 'text': text, 'zodiac_sign_id': zodiac_sign_id}
        horoscope_data.append(entry)

    return horoscope_data


async def man_scrape_horoscopes():
    async with Session as session:
        for horoscope in horoscopes:
            url = horoscope['url']
            zodiac_sign_id = horoscope['zodiac_sign_id']
            horoscope_data = get_horoscope(url, zodiac_sign_id)

            for data in horoscope_data:
                data['id'] = str(uuid.uuid4())

            for data in horoscope_data:
                date = data['date']
                existing_entry = await session.execute(
                    select(ManHoroscopeData).where(ManHoroscopeData.columns.zodiac_sign_id == zodiac_sign_id,
                                                   ManHoroscopeData.columns.date == date)
                )
                if not existing_entry.fetchone():
                    insert_statement = insert(ManHoroscopeData).values(**data, zodiac_sign_id=zodiac_sign_id)
                    await session.execute(insert_statement)

        await session.commit()


async def main():
    await man_scrape_horoscopes()


if __name__ == "__main__":
    asyncio.run(main())
