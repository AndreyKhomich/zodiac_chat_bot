from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

aries = InlineKeyboardButton('Овен', callback_data='знак_Овен')
taurus = InlineKeyboardButton('Телец', callback_data='знак_Телец')
gemini = InlineKeyboardButton('Близнецы', callback_data='знак_Близнецы')
cancer = InlineKeyboardButton('Рак', callback_data='знак_Рак')
leo = InlineKeyboardButton('Лев', callback_data='знак_Лев')
virgo = InlineKeyboardButton('Дева', callback_data='знак_Дева')
libra = InlineKeyboardButton('Весы', callback_data='знак_Весы')
scorpio = InlineKeyboardButton('Скорпион', callback_data='знак_Скорпион')
sagittarius = InlineKeyboardButton('Стрелец', callback_data='знак_Стрелец')
сapricorn = InlineKeyboardButton('Козерог', callback_data='знак_Козерог')
aquarius = InlineKeyboardButton('Водолей', callback_data='знак_Водолей')
pisces = InlineKeyboardButton('Рыбы', callback_data='знак_Рыбы')

inline_kb_full = InlineKeyboardMarkup(row_width=3).add(aries, taurus, gemini, cancer, leo, virgo, libra, scorpio,
                                                       sagittarius, сapricorn, aquarius, pisces)

horoscope = InlineKeyboardButton('Гороскоп', callback_data='меню_Гороскоп')
love_horoscope = InlineKeyboardButton('Любовный гороскоп', callback_data='меню_Любовный_гороскоп')
finance_horoscope = InlineKeyboardButton('Финансовый гороскоп', callback_data='меню_Финансовый_гороскоп')

inline_kb_menu = InlineKeyboardMarkup(row_width=3).add(horoscope).add(love_horoscope).add(finance_horoscope)



