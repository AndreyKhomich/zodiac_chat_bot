import asyncio

from sqlalchemy import insert

from database import async_session_maker
from models.models import ZodiacSign

zodiacs_data = [
    {
        "id": 727,
        "name": "Близнецы"
    },
    {
        "id": 635,
        "name": "Весы"
    },
    {
        "id": 433,
        "name": "Водолей"
    },
    {
        "id": 664,
        "name": "Дева"
    },
    {
        "id": 81,
        "name": "Козерог"
    },
    {
        "id": 978,
        "name": "Лев"
    },
    {
        "id": 449,
        "name": "Овен"
    },
    {
        "id": 288,
        "name": "Рак"
    },
    {
        "id": 310,
        "name": "Рыбы"
    },
    {
        "id": 638,
        "name": "Скорпион"
    },
    {
        "id": 408,
        "name": "Стрелец"
    },
    {
        "id": 571,
        "name": "Телец"
    }
]


async def insert_zodiac_signs():
    async with async_session_maker() as session:
        for zodiac_sign in zodiacs_data:
            insert_statement = insert(ZodiacSign).values(
                id=zodiac_sign['id'],
                name=zodiac_sign['name']
            )
            await session.execute(insert_statement)

        await session.commit()


async def main():
    await insert_zodiac_signs()


if __name__ == "__main__":
    asyncio.run(main())
