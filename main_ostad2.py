#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from requests_forwarder import setup_proxy
setup_proxy(proxy_token="4fcf36959b3ae848d77d7688769180f")

import time
import os

# import random
# import string

# chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

# result = ''.join(random.choices(chars, k=10))
# print(result)

os.makedirs('Data', exist_ok=True)

API_TOKEN = '80467PLgirCKi_ZvGhTG02RQ'

user_steps = dict()         # {cid: step, ...}
user_data = dict()          # {cid: {'first_name': str, 'last_name': str}, ...}
shopping_carts = dict()     # {cid: {pid: qty, ...}, ...}

hideboard = ReplyKeyboardRemove()

bot = telebot.TeleBot(API_TOKEN, num_threads=10)

products = {
    100     :   {'name': "pen", 'desc': "black", 'price': 15, 'file_id': "AgACAgQAAxkBAAIG7WpZ9uydstCRytADYMM5YWTojSoiAAITDmsbqhPQUjIT4eZq0Z3wAQADAgADeAADPQQ"}
}

commands = {
    'start'             :   'start the bot',
    'help'              :   'show help menu',
    'get_info'          :   'get user information',
    'get_keyboard'      :   'show sample keyboard',
    'send_photo'        :   'send sample photo to user',
    'send_document'     :   'send sample doc to user',
    'inlineKeyboard'    :   'send sample inline keyboard to user',
    'send_product'      :   'send product info',
    'show_user_info'    :   'show user information',
    
}


def gen_product_caption(pid, qty=1):
    text = f"""Name: {products[pid]['name']}
Desciption: {products[pid]['desc']}
Price: {products[pid]['price']} $
Total: {products[pid]['price']*qty} $"""
    return text

def gen_product_markup(pid, qty=1):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➖', callback_data=f'change_{pid}_{qty-1}', style='danger'), InlineKeyboardButton(str(qty), callback_data=f'change_{pid}_1', style='primary'), InlineKeyboardButton('➕', callback_data=f'change_{pid}_{qty+1}', style='success'))
    markup.add(InlineKeyboardButton('add to basket', callback_data=f'add_{pid}_{qty}'))
    markup.add(InlineKeyboardButton('cancel', callback_data='cancel'))
    return markup

# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        # print(m)
        if m.content_type == 'text':
            print(f"{m.chat.first_name} [{m.chat.id}]: {m.text}")
        elif m.content_type == 'photo':
            print(f"{m.chat.first_name} [{m.chat.id}]: new photo recieved")
        elif m.content_type == 'document':
            print(f"{m.chat.first_name} [{m.chat.id}]: new document recieved")
            


bot.set_update_listener(listener)  # register listener


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler_method(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    call_id = call.id
    data = call.data
    print(f'cid: {cid}, mid: {mid}, call_id: {call_id}, data: {data}')
    if data.startswith('sample'):    
        print(f'cid: {cid}, mid: {mid}, call_id: {call_id}, data: {data}')
        bot.answer_callback_query(call_id, 'this is answer')
        bot.send_message(cid, f'your sent data was: {data}')
        new_markup = InlineKeyboardMarkup()
        new_markup.add(InlineKeyboardButton('Done ✔', callback_data='nothing'))
        bot.edit_message_reply_markup(cid, mid, reply_markup=new_markup)
    elif data.startswith('change'):
        _, pid, qty = data.split('_')
        if qty == '0':
            bot.answer_callback_query(call_id, 'quantity can not be zero')
            return            
        new_markup = gen_product_markup(int(pid), int(qty))
        bot.edit_message_caption(gen_product_caption(int(pid), int(qty)), cid, mid, reply_markup=new_markup)
        bot.answer_callback_query(call_id, f'quantity changed to {qty}')
    elif data.startswith('add'):
        _, pid, qty = data.split('_')
        shopping_carts.setdefault(cid, dict())
        shopping_carts[cid].setdefault(int(pid), 0)
        shopping_carts[cid][pid] += int(qty)
    elif data == 'nothing':
        bot.answer_callback_query(call_id, 'nothing here')
        


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

@bot.message_handler(commands=['help'])
def command_help_handler(message):
    cid = message.chat.id
    help_text = "You can control me by sending these commands:\n"
    for command, desc in commands.items():
        help_text += f"/{command} - {desc}\n"
    bot.send_message(cid, help_text, reply_to_message_id=message.message_id)
    

@bot.message_handler(commands=['get_info'])
def command_get_info_handler(message):
    cid = message.chat.id
    bot.send_message(cid, "Please wait")
    time.sleep(10)
    bot.send_message(cid, "Please enter your first name:")
    user_steps[cid] = 'A'
    
@bot.message_handler(commands=['get_keyboard'])    
def command_get_keyboard_handler(message):
    cid = message.chat.id
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('button 1', 'button 2')
    bot.send_message(cid, 'here is your keyboard', reply_markup=keyboard)

@bot.message_handler(commands=['send_photo'])
def command_send_photo_handler(message):
    cid = message.chat.id
    bot.send_photo(cid, "AgACAgQAAxkBAAIG0GpZ37COLDvJ2pV4foLRGOuNsQUUAALbDWsbqhPQUp_LV9J-UzH-AQADAgADbQADPQQ")
    # bot.send_photo(cid, "https://imgs.xkcd.com/comics/time_change.png")
    # with open(r"Data\8082244374\photo\17842716467102628.jpg", 'rb') as f:
    #     bot.send_photo(cid, f)
    
@bot.message_handler(commands=['send_document'])
def command_send_document_handler(message):
    cid = message.chat.id
    bot.send_document(cid, "BQACAgQAAxkBAAIGzGpZ3RVnWcnU6-slGpVZZwHy_KXSAALPHAACqhPQUhK6sXcsyaKuPQQ")

@bot.message_handler(commands=['inlineKeyboard'])
def command_inlineKeyboard_handler(message):
    cid = message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('button 1', callback_data='sample_data1'))
    markup.add(InlineKeyboardButton('button 2', callback_data='sample_data2'))
    bot.send_message(cid, 'here is your keybaord', reply_markup=markup)


@bot.message_handler(commands=['send_product'])
def command_send_product_handler(message):
    cid = message.chat.id
    bot.send_photo(cid, products[100]['file_id'], caption=gen_product_caption(100), reply_markup=gen_product_markup(100))

@bot.message_handler(commands=['show_user_info'])
def command_show_user_info_handler(message):
    cid = message.chat.id
    result = bot.get_chat(cid)
    print(result)
    bot.send_message(cid, str(result))

@bot.message_handler(func= lambda m: m.text.startswith('button'))
def button_1_handler(message):
    cid = message.chat.id
    button_no = message.text.split()[-1]
    bot.send_message(cid, f'button {button_no} pressed', reply_markup=hideboard)

@bot.message_handler(func=lambda m: user_steps.get(m.chat.id)=='A')
def user_step_A_handler(message):
    cid = message.chat.id
    first_name = message.text
    bot.send_message(cid, 'Please enter your last name:')
    user_data.setdefault(cid, {'first_name': first_name, 'last_name': ''})
    user_steps[cid] = 'B'

@bot.message_handler(func=lambda m: user_steps.get(m.chat.id)=='B')
def user_step_B_handler(message):
    cid = message.chat.id
    last_name = message.text
    first_name = user_data.get(cid, dict()).get('first_name')
    bot.send_message(cid, f'your full name is: {first_name} {last_name}')
    user_steps.pop(cid)
    user_data.pop(cid)

@bot.message_handler(content_types=['photo'])
def content_photo_handler(message):
    cid = message.chat.id
    file_id = message.photo[-1].file_id
    print(file_id)
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    content = bot.download_file(file_path)
    file_name = str(time.time()).replace('.', '') + '.' + file_path.split('.')[-1]
    file_save_path = os.path.join('Data', str(cid), 'photo')
    os.makedirs(file_save_path, exist_ok=True)
    with open(os.path.join(file_save_path, file_name), 'wb') as f:
        f.write(content)
    bot.send_message(cid, 'photo saved successfully')

@bot.message_handler(content_types=['document'])
def content_document_handler(message):
    cid = message.chat.id
    file_id = message.document.file_id
    file_name = message.document.file_name
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    content = bot.download_file(file_path)
    file_save_path = os.path.join('Data', str(cid), 'document')
    os.makedirs(file_save_path, exist_ok=True)
    with open(os.path.join(file_save_path, file_name), 'wb') as f:
        f.write(content)
    bot.send_message(cid, 'document saved successfully')
        

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()