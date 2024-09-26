import asyncio

from celery import Celery
from database.database_manager import scrape_and_save_horoscope_data, delete_all_horoscopes
from models.models import HoroscopeData, FinanceHoroscopeData, LoveHoroscopeData
from parser.urls_for_parsing import daily_horoscopes, love_horoscopes, finance_horoscopes

app = Celery('celery_app')
app.config_from_object('celeryconfig')


def run_async(func):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(func)


@app.task
def add_horoscope_data():
    result = run_async(scrape_and_save_horoscope_data(HoroscopeData, daily_horoscopes))
    return result


@app.task
def delete_horoscope_data():
    result = run_async(delete_all_horoscopes(HoroscopeData))
    return result


@app.task
def add_love_horoscope_data():
    result = run_async(scrape_and_save_horoscope_data(LoveHoroscopeData, love_horoscopes))
    return result


@app.task
def delete_love_horoscope_data():
    result = run_async(delete_all_horoscopes(LoveHoroscopeData))
    return result


@app.task
def add_finance_horoscope_data():
    result = run_async(scrape_and_save_horoscope_data(FinanceHoroscopeData, finance_horoscopes))
    return result


@app.task
def delete_finance_horoscope_data():
    result = run_async(delete_all_horoscopes(FinanceHoroscopeData))
    return result


app.log.setup(loglevel='DEBUG')
