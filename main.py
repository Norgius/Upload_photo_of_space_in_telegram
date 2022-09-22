import os
import datetime
from urllib.parse import urlsplit
from pathlib import Path

import requests
from dotenv import load_dotenv


Path('images/').mkdir(parents=True, exist_ok=True)
load_dotenv()

headers = {
    'User-Agent': 'My User Agent 1.0'
}


def get_file_extension(link):
    parsed_link = urlsplit(link)
    filename = os.path.split(parsed_link.path)[1]
    return os.path.splitext(filename)[1]


def download_image(url, path, params=None):
    if params is None:
        params = {}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    with open(path, "wb") as file:
        file.write(response.content)


def fetch_spacex_last_launch(id='latest'):
    url_spaceX = f'https://api.spacexdata.com/v5/launches/{id}'
    response = requests.get(url_spaceX, headers=headers)
    response.raise_for_status()
    spacex_links = response.json()["links"]["flickr"].get("original")
    if spacex_links:
        for number, link in enumerate(spacex_links):
            path = Path(f"images/spacex_{number}.jpg")
            download_image(link, path)
    else:
        print("Фотографии с последнего запуска SpaceX отсутствуют")


def fetch_the_best_NASA_photos():
    url_nasa = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": os.getenv("NASA_KEY"), "count": 30}
    response = requests.get(url_nasa, headers=headers, params=params)
    response.raise_for_status()
    for number, dict_data in enumerate(response.json()):
        extension = get_file_extension(dict_data.get("url"))
        if extension:
            path = Path(f'images/nasa_apod_{number}{extension}')
            download_image(dict_data.get("url"), path)


def fetch_nasa_earth_photos():
    url_earth = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": os.getenv("NASA_KEY")}
    response = requests.get(url_earth, headers=headers, params=params)
    response.raise_for_status()

    for number, data_dict in enumerate(response.json()):
        if number == 7:
            break
        date = data_dict.get("date")
        date_for_url = datetime.datetime.fromisoformat(
            date).strftime("%Y/%m/%d")
        filename = data_dict.get("image")
        nasa_earth_link = "https://api.nasa.gov/EPIC/archive/"\
            "natural/{}/png/{}.png".format(date_for_url, filename)
        path = Path(f'images/nasa_earth_{number}.png')
        download_image(nasa_earth_link, path, params)


spacex_id = "5eb87d47ffd86e000604b38a"
fetch_spacex_last_launch(spacex_id)
fetch_the_best_NASA_photos()
fetch_nasa_earth_photos()
