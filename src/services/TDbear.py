import os

from time import sleep
from icecream import ic
from telebot import TeleBot
from telebot import types
from telebot.types import *

from dotenv import load_dotenv

load_dotenv()
bot = TeleBot(os.getenv('BOT_TOKEN'))

@bot.message_handler(commands=['start', 'hello'])
def start(message: Message) -> None:
    ic(message.text)
    
    markup = types.InlineKeyboardMarkup(row_width=5)
    instagram = types.InlineKeyboardButton('Instagram', callback_data='instagram')
    pinterest = types.InlineKeyboardButton('pinterest', callback_data='pinterest')

    markup.add(instagram, pinterest)

    ic(type(message))
    bot.send_message(message.chat.id, 'choose social media', reply_markup=markup)
    ...

@bot.callback_query_handler(func=lambda call:True)
def answer(callback: CallbackQuery) -> None:

    if callback.message:

        match callback.data:
            case 'instagram':
                bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
                chat_id = callback.message.chat.id

                bot.send_message(chat_id, "Insert target username: ")
                @bot.message_handler(func=lambda message: message.chat.id == chat_id)
                def handle(message):
                    ic(message.text)
                    bot.send_message(chat_id=message.chat.id,
                                     text=message.text)
                    
                    format = types.InlineKeyboardMarkup(row_width=5)
                    image = types.InlineKeyboardButton('image', callback_data='image')
                    video = types.InlineKeyboardButton('video', callback_data='video')
                    all = types.InlineKeyboardButton('all', callback_data='all')

                    format.add(image, video, all)

                    ic(type(message))
                    bot.send_message(message.chat.id, 'choose format', reply_markup=format)
                    ic("done")

                ...

            case 'pinterest':
                bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=callback.data
                )
                ...
    ...

def instagram(chat_id, context) -> None:
    bot.send_message(
        chat_id=chat_id,
            text='insert target username!'
        )

bot.infinity_polling()