import os
from urllib.parse import urlsplit
from pathlib import Path

import requests
from dotenv import load_dotenv


Path('images').mkdir(parents=True, exist_ok=True)
load_dotenv()

headers = {
    'User-Agent': 'My User Agent 1.0'
}


def get_file_extension(link):
    parsed_link = urlsplit(link)
    filename = os.path.split(parsed_link.path)[1]
    return os.path.splitext(filename)[1]


def download_image(url, path, params=None):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)
