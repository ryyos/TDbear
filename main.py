import os

from time import sleep
from icecream import ic
from telebot import TeleBot
from telebot import types
from telebot.types import *
from concurrent.futures import ThreadPoolExecutor, wait

from dotenv import load_dotenv
from src.services.instagram import Instagram

harvest = Instagram()
executor = ThreadPoolExecutor()

load_dotenv()
bot = TeleBot(os.getenv('BOT_TOKEN'))

fiture = ['instagram', 'pinterest']
formats = ['image', 'video', 'all']

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

@bot.callback_query_handler(func=lambda call: call.data in fiture)
def answer(callback: CallbackQuery) -> None:

    if callback.message:

        ic('terpanggil')

        global category
        category = callback.data

        match callback.data:
            case 'instagram':
                bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)

                chat_id = callback.message.chat.id

                bot.send_message(chat_id, "Insert target username: ")
                @bot.message_handler(func=lambda message: message.chat.id == chat_id)
                def handle(message):

                    global username
                    username = message.text

                    bot.send_message(chat_id=message.chat.id,
                                     text=message.text)
                    
                    format = types.InlineKeyboardMarkup(row_width=5)
                    image = types.InlineKeyboardButton('image', callback_data='image')
                    video = types.InlineKeyboardButton('video', callback_data='video')
                    all = types.InlineKeyboardButton('all', callback_data='all')

                    format.add(image, video, all)
                    ic('memilih format')
                    bot.send_message(message.chat.id, 'choose format', reply_markup=format)
                    ic('hehe')
                    
                ...

            case 'pinterest':
                bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=callback.data
                )

            case 'pinterest':
                bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=callback.data
                )
                ...
    ...

def send(component: dict) -> None:
    try: bot.send_photo(chat_id=component["callback"].message.chat.id, photo=component["url"])
    except Exception: bot.send_video(chat_id=component["callback"].message.chat.id, video=component["url"]) 

@bot.callback_query_handler(func=lambda call: call.data in formats)
def hanlde_format(callback: CallbackQuery) -> None:
    ic('masuk handle format')
    if callback.message:
        match category:
            case 'instagram':
                bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)


                task_executor = []
                for url in harvest.main(username=username, format=callback.data):
                    task_executor.append(executor.submit(send, {
                        "callback": callback,
                        "url": url
                    }))

                wait(task_executor)

        
        ...

bot.infinity_polling()