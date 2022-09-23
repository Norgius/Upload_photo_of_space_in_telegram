from random import shuffle
from telegram import InputMediaPhoto
import telegram
import argparse
import time
import os

from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
Path('images/').mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser(
    description='''Интервал публикации изображений в \
                   телеграм канале, по умолчанию - 4 часа'''
)
parser.add_argument('-t', '--time', default=None, type=int,
                    help='Частота публикаций')
args = parser.parse_args()
if args.time:
    interval = args.time * 3600
else:
    interval = 14400

bot = telegram.Bot(token=os.getenv('TELEGRAM_SPACE_BOT'))

while True:
    images = list(os.walk(Path("images/")))[0][2]
    if not images:
        print("Изображения отсутствуют, пожалуйста загрузите их")
        break
    shuffle(images)
    for image in images:
        photo = InputMediaPhoto(media=open(Path(f"images/{image}"), "rb"))
        bot.send_media_group(chat_id='@space_photos_prime',
                             media=[photo])
        time.sleep(interval)
