from utils_and_download_image import headers, download_image
import argparse

import requests
from pathlib import Path


spacex_id = "5eb87d47ffd86e000604b38a"


def fetch_spacex_last_launch(id='latest'):
    try:
        url_spaceX = f'https://api.spacexdata.com/v5/launches/{id}'
        response = requests.get(url_spaceX, headers=headers)
        response.raise_for_status()
        spacex_links = response.json()["links"]["flickr"].get("original")

        if spacex_links:
            for number, link in enumerate(spacex_links):
                path = Path(f"images/spacex_{number}.jpg")
                download_image(link, path)
        else:
            print("Фотографии с последнего запуска SpaceX "
                  "отсутствуют, пожалуйста передайте в "
                  "аргумент программы id запуска ракеты.")
    except requests.exceptions.HTTPError:
        raise TypeError("Данного id не существует")


parser = argparse.ArgumentParser(
    description='''Данная программа позволяет скачивать \
                    фотографии с запусков ракет SpaceX'''
)
parser.add_argument('--id', default=None, type=str,
                    help='id запуска ракеты')
args = parser.parse_args()
if args.id:
    fetch_spacex_last_launch(args.id)
else:
    fetch_spacex_last_launch()
