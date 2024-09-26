import uuid

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

User = Table(
    'users',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

ZodiacSign = Table(
    'zodiac_signs',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
)


HoroscopeData = Table(
    'horoscope_data',
    metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("date", String),
    Column("text", String),
    Column("zodiac_sign_id", Integer, ForeignKey('zodiac_signs.id')),
)


LoveHoroscopeData = Table(
    'love_horoscope_data',
    metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("date", String),
    Column("text", String),
    Column("zodiac_sign_id", Integer, ForeignKey('zodiac_signs.id')),
)

FinanceHoroscopeData = Table(
    'finance_horoscope_data',
    metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("date", String),
    Column("text", String),
    Column("zodiac_sign_id", Integer, ForeignKey('zodiac_signs.id')),
)
