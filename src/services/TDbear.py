import os

from icecream import ic
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()

bot = TeleBot(os.getenv('BOT_TOKEN'))
class TDbear:

    @bot.message_handler(commands=['start', 'hello'])
    def start(message):
        ic(message.text)
        bot.reply_to(message, text='Sabar hehe')
        ...


bot.infinity_polling()