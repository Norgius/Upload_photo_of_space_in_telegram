from utils_and_download_image import headers, download_image
import argparse
import os

import requests


spacex_id = '5eb87d47ffd86e000604b38a'


def fetch_spacex_last_launch(id):
    url_spaceX = f'https://api.spacexdata.com/v5/launches/{id}'
    response = requests.get(url_spaceX, headers=headers)
    response.raise_for_status()
    spacex_links = response.json()['links']['flickr'].get('original')
    for number, link in enumerate(spacex_links):
        path = os.path.join('images', f'spacex_{number}.jpg')
        download_image(link, path)


def main():
    parser = argparse.ArgumentParser(
        description='''Данная программа позволяет скачивать \
                        фотографии с запусков ракет SpaceX'''
    )
    parser.add_argument('-id', default='latest',
                        type=fetch_spacex_last_launch,
                        help='id запуска ракеты')
    try:
        args = parser.parse_args()
        args.id
    except requests.exceptions.HTTPError:
        raise TypeError('Данного id не существует')


if __name__ == '__main__':
    main()
    print('Фотографии SpaceX загружены')
