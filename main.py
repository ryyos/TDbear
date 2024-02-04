import os
import asyncio

from time import sleep
from icecream import ic
from dotenv import load_dotenv

from telebot import TeleBot
from telebot import types
from telebot.types import *

from src.services.instagram import Instagram
from src.services.pinterest import Pinterest
from src.services.cockroachDB import CokroachDB
from src.PyCharacterAI import Client

harvest = Instagram()
pinrys = Pinterest()
cock = CokroachDB()


async def askAi(message):
    client = Client()
    await client.authenticate_with_token(os.getenv('AI_TOKEN'))

    username = (await client.fetch_user())['user']['username']
    print(f'Authenticated as {username}')
    chat = await client.create_or_continue_chat(os.getenv('CHAR_ID'))

    answer = await chat.send_message(message)
    return answer.text

load_dotenv()
bot = TeleBot(os.getenv('BOT_TOKEN'))

fiture = ['instagram', 'pinterest', 'twiter']
formats = ['image', 'video', 'all']
totals = ['10', '50', '100', '250', 'custom']

@bot.message_handler(commands=['start', 'hello'])
def start(message: Message) -> None:

    ic(message.text)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    instagram = types.InlineKeyboardButton('Instagram', callback_data='instagram')
    pinterest = types.InlineKeyboardButton('pinterest', callback_data='pinterest')
    twiter = types.InlineKeyboardButton('twiter', callback_data='twiter')

    markup.add(instagram, pinterest, twiter)

    bot.send_message(message.chat.id, 'choose social media', reply_markup=markup)
    ...

@bot.message_handler(commands=['AI'])
def ai(message: Message) -> None:
    intro = f'hai, namaku {message.chat.username}.. bisakah kamu menyapaku dan perkenalkan dirimu dengan bahasa indonesia?'
    ic(intro)
    bot.send_message(chat_id=message.chat.id,
                        text=asyncio.run(askAi(intro)))
    ...



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(callback: CallbackQuery) -> None:
    if callback.data in fiture:

        global sessions
        sessions = callback.data

        match callback.data:
            case 'instagram':
                bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
                bot.send_message(callback.message.chat.id, "Insert target Instagram username")

                ...

            case 'pinterest':
                global key_search
                key_search = None
                bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
                bot.send_message(callback.message.chat.id, "what image do you want to search.?")
    

            case 'twiter':
                bot.send_message(
                    chat_id=callback.message.chat.id,
                    text='Sabar belum jadi bang hehe'
                )

    elif callback.data in formats:
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)

        amount = 0
        for url in harvest.main(username=username, format=callback.data):
            try: bot.send_photo(chat_id=callback.message.chat.id, photo=url)
            except Exception: bot.send_video(chat_id=callback.message.chat.id, video=url)
            finally: amount+=1

        user = bot.get_chat(callback.message.chat.id)
        cock.send({
            "id": callback.message.message_id,
            "user_id": callback.message.chat.id,
            "username": user.username,
            "bio": user.bio,
            "amount": amount,
            "action": sessions,
            "key_search": username
        })

    
    elif callback.data in totals:
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)

        try:
            for url in pinrys.main(name=key_search, size=int(callback.data)):
                try: bot.send_photo(chat_id=callback.message.chat.id, photo=url)
                except Exception: bot.send_video(chat_id=callback.message.chat.id, video=url) 

            user = bot.get_chat(callback.message.chat.id)
            cock.send({
                "id": callback.message.message_id,
                "user_id": callback.message.chat.id,
                "username": user.username,
                "bio": user.bio,
                "amount": int(callback.data),
                "action": sessions,
                "key_search": username
            })
        except Exception:
            bot.send_message(callback.message.chat.id, "Insert count")
    ...

@bot.message_handler(func=lambda message: True)
def message_handle(message: Message):
    global username

    if message.text.startswith('$'):
        bot.send_message(chat_id=message.chat.id,
                         text=asyncio.run(askAi(message.text)))

    try:

        total = int(message.text)
        ic(total)
        ic(sessions)
        match sessions:
            case 'instagram':
                ...

            case 'pinterest':
                global key_search
                for url in pinrys.main(name=key_search, size=int(message.text)):
                    try: bot.send_photo(chat_id=message.chat.id, photo=url)
                    except Exception: bot.send_video(chat_id=message.chat.id, video=url)

                user = bot.get_chat(message.chat.id)
                cock.send({
                    "id": message.message_id,
                    "user_id": message.chat.id,
                    "username": user.username,
                    "bio": user.bio,
                    "amount": int(message.text),
                    "action": sessions,
                    "key_search": username
                })

    except Exception as err:

        ic(err)

        match sessions:
            case 'instagram':
                username = message.text
                
                format = types.InlineKeyboardMarkup(row_width=2)
                image = types.InlineKeyboardButton('image', callback_data='image')
                video = types.InlineKeyboardButton('video', callback_data='video')
                all = types.InlineKeyboardButton('all', callback_data='all')

                format.add(image, video, all)
                bot.send_message(message.chat.id, 'choose format', reply_markup=format)

            case 'pinterest':
                key_search = message.text

                total = types.InlineKeyboardMarkup(row_width=2)
                ten = types.InlineKeyboardButton('10', callback_data='10')
                fifty = types.InlineKeyboardButton('50', callback_data='50')
                hundred = types.InlineKeyboardButton('100', callback_data='100')
                maximal = types.InlineKeyboardButton('250', callback_data='250')
                custom = types.InlineKeyboardButton('custom', callback_data='custom')

                total.add(ten, fifty, hundred, maximal, custom)
                bot.send_message(message.chat.id, 'input amount (250 max)', reply_markup=total)

        
bot.infinity_polling()