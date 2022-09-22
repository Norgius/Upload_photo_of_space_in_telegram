import telegram
import os

from dotenv import load_dotenv


load_dotenv()

bot = telegram.Bot(token=os.getenv('TELEGRAM_SPACE_BOT'))
bot.send_message(text='Hi John!', chat_id='@space_photos_prime')
