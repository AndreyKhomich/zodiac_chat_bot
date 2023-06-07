import json

import requests
from bs4 import BeautifulSoup


def get_horoscope(url, filename):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }

    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    src = r.text

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(src)

    with open(filename, 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, "html.parser")
    decode_text = soup.get_text()

    # Find all the date elements (i.e., <i> tags with class "sprl")
    date_elements = soup.find_all('i', class_='sprl')

    # Extract the date and text for each element
    data = []
    for date_element in date_elements:
        date = date_element.text.strip()
        text = date_element.find_next_sibling('div').text.strip()
        entry = {'date': date, 'text': text}
        data.append(entry)

    with open(f'{filename}_json.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    with open(f'{filename}_json.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    days_to_remove = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    filtered_data = []
    for entry in data:
        date = entry['date']
        text = entry['text']
        for day in days_to_remove:
            date = date.replace(day + ", ", "")
        filtered_entry = {'date': date, 'text': text}
        filtered_data.append(filtered_entry)

    # Save the filtered data to a new JSON file
    with open(f'{filename}_json.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, indent=4, ensure_ascii=False)


# URLs and filenames for different horoscopes
horoscopes = [
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/skorpion-nedelya.html',
        'filename': 'zodiacs_data/Скорпион/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/vesy-nedelya.html',
        'filename': 'zodiacs_data/Весы/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/strelets-nedelya.html',
        'filename': 'zodiacs_data/Стрелец/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/kozerog-nedelya.html',
        'filename': 'zodiacs_data/Козерог/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/vodolej-nedelya.html',
        'filename': 'zodiacs_data/Водолей/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/ryby-nedelya.html',
        'filename': 'zodiacs_data/Рыбы/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/oven-nedelya.html',
        'filename': 'zodiacs_data/Овен/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/telets-nedelya.html',
        'filename': 'zodiacs_data/Телец/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/bliznetsy-nedelya.html',
        'filename': 'zodiacs_data/Близнецы/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/rak-nedelya.html',
        'filename': 'zodiacs_data/Рак/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/lev-nedelya.html',
        'filename': 'zodiacs_data/Лев/index.html'
    },
    {
        'url': 'https://gadalkindom.ru/goroskop/nedelya/deva-nedelya.html',
        'filename': 'zodiacs_data/Дева/index.html'
    },
]

for horoscope in horoscopes:
    get_horoscope(horoscope['url'], horoscope['filename'])
