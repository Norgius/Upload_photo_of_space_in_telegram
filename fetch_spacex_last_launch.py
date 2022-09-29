from utils_and_download_image import HEADERS, download_image
from pathlib import Path
import argparse
import os

import requests


def fetch_spacex_last_launch(id):
    url_spaceX = f'https://api.spacexdata.com/v5/launches/{id}'
    response = requests.get(url_spaceX, headers=HEADERS)
    response.raise_for_status()
    spacex_links = response.json()['links']['flickr'].get('original')
    if not spacex_links:
        raise TypeError('Фотографии с последнего запуска SpaceX '
                        'отсутствуют, пожалуйста передайте в '
                        'аргумент программы id запуска ракеты.')
    for number, link in enumerate(spacex_links):
        path = os.path.join('images', f'spacex_{number}.jpg')
        download_image(link, path)


def main():
    Path('images').mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(
        description='''Данная программа позволяет скачивать \
                        фотографии с запусков ракет SpaceX'''
    )
    parser.add_argument('-id', default='latest',
                        help='id запуска ракеты')
    try:
        args = parser.parse_args()
        fetch_spacex_last_launch(args.id)
        print('Фотографии SpaceX загружены')
    except requests.exceptions.HTTPError:
        raise TypeError('Данного id не существует')


if __name__ == '__main__':
    main()
