from random import shuffle, choice
from pathlib import Path
import argparse
import time
import os

import telegram
from telegram import InputMediaPhoto
from dotenv import load_dotenv


Path('images').mkdir(parents=True, exist_ok=True)


def check_files():
    for _, _, files in os.walk('images'):
        files = files
    if not files:
        raise TypeError('Изображения отсутствуют, пожалуйста загрузите их')
    return files


def post_one_photo(token, filename=''):
    files = check_files()
    if not filename:
        filename = choice(files)
    if filename not in files:
        return 'Данный файл отсутствует в images'
    bot = telegram.Bot(token=token)
    photo = InputMediaPhoto(media=open(
            os.path.join('images', filename), 'rb')
    )
    bot.send_media_group(chat_id='@space_photos_prime',
                         media=[photo])
    return 'Фотография опубликована'


def post_endlessly(token):
    bot = telegram.Bot(token=token)
    while True:
        files = check_files()
        shuffle(files)
        for filename in files:
            photo = InputMediaPhoto(media=open(
                        os.path.join('images', filename), 'rb'))
            bot.send_media_group(chat_id='@space_photos_prime',
                                 media=[photo])
            time.sleep(14400)


def main(token):
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
    if args.photo == 'cycle':
        return post_endlessly(token)
    elif args.photo:
        return post_one_photo(token, args.photo)
    else:
        return post_one_photo(token)


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TELEGRAM_SPACE_BOT')
    print(main(token))
