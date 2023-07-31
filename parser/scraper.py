import requests
from bs4 import BeautifulSoup


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
