from utils_and_download_image import headers, download_image
from utils_and_download_image import get_file_extension
from pathlib import Path
import argparse
import os

import requests


def fetch_apod_NASA_photos(api_key, number):
    url_nasa = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': api_key, 'count': int(number)}
    response = requests.get(url_nasa, headers=headers, params=params)
    response.raise_for_status()

    for counter, dict_data in enumerate(response.json()):
        extension = get_file_extension(dict_data.get('url'))
        if extension:
            path = Path(f'images/nasa_apod_{counter}{extension}')
            download_image(dict_data.get('url'), path)
    return 'Фотографии APOD NASA загружены'


def main(api_key):
    parser = argparse.ArgumentParser(
        description='Данная программа позволяет '
                    'скачивать apod фотографии NASA'
    )
    parser.add_argument('-n', default='10',
                        help='''Число для загрузки нужного \
                                количества фотографий''')
    args = parser.parse_args()
    return fetch_apod_NASA_photos(api_key, args.n)


if __name__ == '__main__':
    api_key = os.getenv('NASA_KEY')
    print(main(api_key))
