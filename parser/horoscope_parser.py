import asyncio
from database.database_manager import scrape_and_save_horoscope_data, delete_all_horoscopes
from models.models import HoroscopeData, FinanceHoroscopeData, LoveHoroscopeData
from parser.urls_for_parsing import daily_horoscopes, love_horoscopes, finance_horoscopes


async def run():
    await scrape_and_save_horoscope_data(HoroscopeData, daily_horoscopes)
    # await delete_all_horoscopes(HoroscopeData)
    await scrape_and_save_horoscope_data(FinanceHoroscopeData, finance_horoscopes)
    # await delete_all_horoscopes(FinanceHoroscopeData)
    await scrape_and_save_horoscope_data(LoveHoroscopeData, love_horoscopes)
    # await delete_all_horoscopes(LoveHoroscopeData)

if __name__ == "__main__":
    asyncio.run(run())
