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
load_dotenv()

harvest = Instagram()
pinrys = Pinterest()
cock = CokroachDB()
bot = TeleBot(os.getenv('BOT_TOKEN'))


fiture = ['instagram', 'pinterest', 'twiter']
formats = ['image', 'video', 'all']
totals = ['10', '50', '100', '250', 'custom']

session = None
username = None

async def askAi(message):
    client = Client()
    await client.authenticate_with_token(os.getenv('AI_TOKEN'))

    username = (await client.fetch_user())['user']['username']
    print(f'Authenticated as {username}')
    chat = await client.create_or_continue_chat(os.getenv('CHAR_ID'))

    answer = await chat.send_message(message)
    return answer.text

@bot.message_handler(commands=['tdbear'])
def start(message: Message) -> None:

    ic(message.text)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    instagram = types.InlineKeyboardButton('Instagram', callback_data='instagram')
    pinterest = types.InlineKeyboardButton('pinterest', callback_data='pinterest')
    twiter = types.InlineKeyboardButton('twiter', callback_data='twiter')

    markup.add(instagram, pinterest, twiter)

    bot.send_message(message.chat.id, 'choose social media', reply_markup=markup)
    ...

@bot.message_handler(commands=['start'])
def start(message: Message) -> None:

    text = """
Command list
/start  : showing what the bot can do 
/tdbear : to download images from social media
/AI     : to chat with AI
/info   : information about bots

/license : license
/admin   : admin mode
        """ 

    bot.send_message(chat_id=message.chat.id, 
                     text=f'hello {message.chat.username} 👋')
    
    bot.send_message(chat_id=message.chat.id, 
                     text=text)

    user = bot.get_chat(message.chat.id)
    cock.send({
        "id": message.message_id,
        "user_id": message.chat.id,
        "username": user.username,
        "bio": user.bio,
        "amount": None,
        "format": None,
        "action": 'start',
        "key_search": None
    })

    
    ...

@bot.message_handler(commands=['info'])
def info(message: Message) -> None:

    jiko = f"""
hello {message.chat.username}👋, 
I am your assistant cavalencia-bot, 
my creator gave me that name because it comes 
from JKT48 member catherine valencia
        """ 
    
    lic = """
this project is licensed under an MIT LICENSE

/license for more details
        """

    bot.send_message(chat_id=message.chat.id, 
                     text=jiko)
    
    bot.send_message(chat_id=message.chat.id, 
                     text=lic)
    
    user = bot.get_chat(message.chat.id)
    cock.send({
        "id": message.message_id,
        "user_id": message.chat.id,
        "username": user.username,
        "bio": user.bio,
        "amount": None,
        "format": None,
        "action": 'info',
        "key_search": None
    })

    ...

@bot.message_handler(commands=['license'])
def license(message: Message) -> None:

    bot.send_photo(chat_id=message.chat.id,
                    photo=open('LICENSE.jpg', 'rb'),
                    caption='https://opensource.org/license/mit/')

    user = bot.get_chat(message.chat.id)
    cock.send({
        "id": message.message_id,
        "user_id": message.chat.id,
        "username": user.username,
        "bio": user.bio,
        "amount": None,
        "format": None,
        "action": 'license',
        "key_search": None
    })
    ...

@bot.message_handler(commands=['admin'])
def license(message: Message) -> None:

    bot.send_message(chat_id=message.chat.id,
                        text='You are not allowed')

@bot.message_handler(commands=['AI'])
def ai(message: Message) -> None:
    intro = f'hai, namaku {message.chat.username}.. bisakah kamu menyapaku dan perkenalkan dirimu dengan bahasa indonesia?'
    ic(intro)
    answer = asyncio.run(askAi(intro))
    bot.send_message(chat_id=message.chat.id,
                        text=answer)
    
    user = bot.get_chat(message.chat.id)
    cock.send({
        "id": message.message_id,
        "user_id": message.chat.id,
        "username": user.username,
        "bio": user.bio,
        "action": 'ai',
        "question": None,
        "answer": answer
    })
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
        try:
            for url in harvest.main(username=username, format=callback.data):
                if '#inifoto' in url: bot.send_photo(chat_id=callback.message.chat.id, photo=url.replace('#inifoto', ''))
                else: bot.send_video(chat_id=callback.message.chat.id, video=url)
                amount+=1

        except Exception as err:
            bot.send_message(callback.message.chat.id, err)

        user = bot.get_chat(callback.message.chat.id)
        cock.send({
            "id": callback.message.message_id,
            "user_id": callback.message.chat.id,
            "username": user.username,
            "bio": user.bio,
            "format": callback.data,
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
                "format": 'image',
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
        answer = asyncio.run(askAi(message.text))
        bot.send_message(chat_id=message.chat.id,
                         text=answer)
                
        user = bot.get_chat(message.chat.id)
        cock.send({
            "id": message.message_id,
            "user_id": message.chat.id,
            "username": user.username,
            "bio": user.bio,
            "action": 'ai',
            "question": message.text,
            "answer": answer
        })
    try:

        total = int(message.text)
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
                    "format": 'image',
                    "amount": int(message.text),
                    "action": sessions,
                    "key_search": key_search
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