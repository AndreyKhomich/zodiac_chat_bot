import os
import json
import random
import uuid

# Define the path to the folder containing the zodiac data
zodiacs_folder = "zodiacs_data"


def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json_file(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def process_zodiac_data():
    zodiac_signs_file_path = "zodiac_signs.json"
    zodiac_signs_data = read_json_file(zodiac_signs_file_path)

    for zodiac_sign in zodiac_signs_data:
        zodiac_id = zodiac_sign["id"]
        zodiac_name = zodiac_sign["name"]

        folder_name = str(zodiac_name)
        folder_path = os.path.join(zodiacs_folder, folder_name)

        json_file_path = os.path.join(folder_path, "index.html_json.json")
        horoscope_data = read_json_file(json_file_path)

        horoscope_data_list = []
        for data in horoscope_data:
            horoscope_id = horoscope_id = str(uuid.uuid4())

            horoscope_data_dict = {
                "id": horoscope_id,
                "date": data["date"],
                "text": data["text"],
                "zodiac_sign_id": zodiac_id
            }
            horoscope_data_list.append(horoscope_data_dict)

        horoscope_data_file_path = os.path.join(folder_path, "horoscope_data.json")
        write_json_file(horoscope_data_list, horoscope_data_file_path)


if __name__ == "__main__":
    process_zodiac_data()
