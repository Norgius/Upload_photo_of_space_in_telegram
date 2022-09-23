from utils_and_download_image import headers, download_image
from pathlib import Path
import datetime
import os

import requests


def fetch_nasa_earth_photos():
    url_earth = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": os.getenv("NASA_KEY")}
    response = requests.get(url_earth, headers=headers, params=params)
    response.raise_for_status()

    for counter, data_dict in enumerate(response.json()):
        if counter == 7:
            break
        date = data_dict.get("date")
        date_for_url = datetime.datetime.fromisoformat(
            date).strftime("%Y/%m/%d")
        filename = data_dict.get("image")
        nasa_earth_link = "https://api.nasa.gov/EPIC/archive/"\
            "natural/{}/png/{}.png".format(date_for_url, filename)
        path = Path(f'images/nasa_earth_{counter}.png')
        download_image(nasa_earth_link, path, params)


fetch_nasa_earth_photos()
