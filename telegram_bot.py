from random import shuffle, choice
from pathlib import Path
import argparse
import time
import os

import telegram
from telegram import InputMediaPhoto
from dotenv import load_dotenv


load_dotenv()
Path('images/').mkdir(parents=True, exist_ok=True)


def check_files():
    files = list(os.walk(Path("images/")))[0][2]
    if not files:
        raise TypeError("Изображения отсутствуют, пожалуйста загрузите их")
    return files


def post_one_photo(filename=''):
    files = check_files()
    if not filename:
        filename = choice(files)
    if filename not in files:
        print("Данный файл отсутствует в images/")
        return
    photo = InputMediaPhoto(media=open(Path(f"images/{filename}"), "rb"))
    bot.send_media_group(chat_id='@space_photos_prime',
                         media=[photo])


def post_endlessly():
    while True:
        files = check_files()
        shuffle(files)
        for filename in files:
            photo = InputMediaPhoto(media=open(
                        Path(f"images/{filename}"), "rb"))
            bot.send_media_group(chat_id='@space_photos_prime',
                                 media=[photo])
            time.sleep(14400)


parser = argparse.ArgumentParser(
    description='''Публикует в телеграм канале отдельное фото, \
                   случайное фото или публикует фотографии в \
                   бесконечном цикле с интервалом 4 часа'''
)
parser.add_argument('-p', '--photo', default=None, type=str,
                    help='''-p cycle - бесконечный цикл;
                         -p [filename] - публикация фото filename;
                         без аргументов - публикация случайного фото'''
                    )
args = parser.parse_args()
bot = telegram.Bot(token=os.getenv('TELEGRAM_SPACE_BOT'))
if args.photo == 'cycle':
    post_endlessly()
elif args.photo:
    post_one_photo(args.photo)
else:
    post_one_photo()
