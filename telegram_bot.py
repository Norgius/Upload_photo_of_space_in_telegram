from random import shuffle, choice
from pathlib import Path
import argparse
import time
import os

import telegram
from telegram import InputMediaPhoto
from dotenv import load_dotenv


def get_files_path():
    for _, _, files in os.walk('images'):
        files = files
    if not files:
        raise TypeError('Изображения отсутствуют, пожалуйста загрузите их')
    return files


def post_one_photo(token, chat_id, filename=''):
    files = get_files_path()
    if not filename:
        filename = choice(files)
    if filename not in files:
        raise TypeError('Данный файл отсутствует в images')
    bot = telegram.Bot(token=token)
    with open(os.path.join('images', filename), 'rb') as filename:
        photo = InputMediaPhoto(media=filename)
    bot.send_media_group(chat_id=chat_id, media=[photo])


def post_endlessly(token, chat_id):
    bot = telegram.Bot(token=token)
    while True:
        files = get_files_path()
        shuffle(files)
        for filename in files:
            with open(os.path.join('images', filename), 'rb') as filename:
                photo = InputMediaPhoto(media=filename)
            bot.send_media_group(chat_id=chat_id, media=[photo])
            time.sleep(14400)


def main():
    load_dotenv()
    Path('images').mkdir(parents=True, exist_ok=True)
    token = os.getenv('SPACE_BOT_TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
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
        post_endlessly(token, chat_id)
    elif args.photo:
        post_one_photo(token, chat_id, args.photo)
    else:
        post_one_photo(token, chat_id)


if __name__ == '__main__':
    main()
    print('Фотография опубликована')
