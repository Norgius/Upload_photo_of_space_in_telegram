from utils_and_download_image import headers, download_image
from pathlib import Path
import datetime
import os

import requests


def main(api_key):
    url_earth = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}
    response = requests.get(url_earth, headers=headers, params=params)
    response.raise_for_status()

    for counter, response_part in enumerate(response.json()):
        if counter == 7:
            break
        date = response_part.get("date")
        date_for_url = datetime.datetime.fromisoformat(
            date).strftime("%Y/%m/%d")
        filename = response_part.get("image")
        nasa_earth_link = "https://api.nasa.gov/EPIC/archive/"\
            "natural/{}/png/{}.png".format(date_for_url, filename)
        path = Path(f'images/nasa_earth_{counter}.png')
        download_image(nasa_earth_link, path, params)
    return "Фотографии нашей планеты загружены"


if __name__ == '__main__':
    api_key = os.getenv("NASA_KEY")
    print(main(api_key))
