from telegram import InputMediaPhoto
import telegram
import os

from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

bot = telegram.Bot(token=os.getenv('TELEGRAM_SPACE_BOT'))

media_1 = InputMediaPhoto(media=open(Path("images/nasa_apod_0.jpg"), "rb"))
bot.send_media_group(chat_id='@space_photos_prime',
                     media=[media_1])
