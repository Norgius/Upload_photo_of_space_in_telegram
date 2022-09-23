from utils_and_download_image import headers, download_image
from utils_and_download_image import get_file_extension
from pathlib import Path
import argparse
import os

import requests


def fetch_apod_NASA_photos(number=10):
    url_nasa = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": os.getenv("NASA_KEY"), "count": number}
    response = requests.get(url_nasa, headers=headers, params=params)
    response.raise_for_status()

    for counter, dict_data in enumerate(response.json()):
        extension = get_file_extension(dict_data.get("url"))
        if extension:
            path = Path(f'images/nasa_apod_{counter}{extension}')
            download_image(dict_data.get("url"), path)


parser = argparse.ArgumentParser(
    description='Данная программа позволяет '
                'скачивать apod фотографии NASA'
)
parser.add_argument('-n', '--number', default=None, type=int,
                    help='''Число для загрузки нужного \
                            количества фотографий''')
args = parser.parse_args()
if args.number:
    fetch_apod_NASA_photos(args.number)
else:
    fetch_apod_NASA_photos()
