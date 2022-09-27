from utils_and_download_image import HEADERS, download_image
from pathlib import Path
import datetime
import argparse
import os

import requests
from dotenv import load_dotenv


def fetch_nasa_earth_photos(api_key, number):
    url_earth = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': api_key}
    response = requests.get(url_earth, headers=HEADERS, params=params)
    response.raise_for_status()
    for counter, response_part in enumerate(response.json()):
        if counter == number:
            break
        date = response_part.get('date')
        date_for_url = datetime.datetime.fromisoformat(
            date).strftime('%Y/%m/%d')
        filename = response_part.get('image')
        nasa_earth_link = 'https://api.nasa.gov/EPIC/archive/'\
            'natural/{}/png/{}.png'.format(date_for_url, filename)
        path = os.path.join('images', f'nasa_earth_{counter}.png')
        download_image(nasa_earth_link, path, params)


def main():
    load_dotenv()
    Path('images').mkdir(parents=True, exist_ok=True)
    api_key = os.getenv('NASA_KEY')
    parser = argparse.ArgumentParser(
        description='Данная программа позволяет '
                    'скачивать фотографии нашей планеты'
    )
    parser.add_argument('-n', default='7', type=int,
                        help='''Число для загрузки нужного \
                                количества фотографий (от 1 до 10)''')
    args = parser.parse_args()
    fetch_nasa_earth_photos(api_key, args.n)


if __name__ == '__main__':
    main()
    print('Фотографии нашей планеты загружены')
