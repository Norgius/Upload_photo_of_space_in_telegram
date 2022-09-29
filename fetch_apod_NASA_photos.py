from utils_and_download_image import HEADERS, download_image
from utils_and_download_image import get_file_extension
from pathlib import Path
import argparse
import os

import requests
from dotenv import load_dotenv


def fetch_apod_NASA_photos(api_key, number):
    url_nasa = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': api_key, 'count': number}
    response = requests.get(url_nasa, headers=HEADERS, params=params)
    response.raise_for_status()

    for counter, response_part in enumerate(response.json()):
        extension = get_file_extension(response_part.get('url'))
        if extension:
            path = os.path.join('images', f'nasa_apod_{counter}{extension}')
            download_image(response_part.get('url'), path)


def main():
    load_dotenv()
    Path('images').mkdir(parents=True, exist_ok=True)
    api_key = os.getenv('NASA_KEY')
    parser = argparse.ArgumentParser(
        description='Данная программа позволяет '
                    'скачивать apod фотографии NASA'
    )
    parser.add_argument('-n', default='10', type=int,
                        help='''Число для загрузки нужного \
                                количества фотографий''')
    args = parser.parse_args()
    fetch_apod_NASA_photos(api_key, args.n)
    print('Фотографии APOD NASA загружены')


if __name__ == '__main__':
    main()
