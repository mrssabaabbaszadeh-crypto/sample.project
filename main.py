#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from requests_forwarder import setup_proxy
setup_proxy(proxy_token="4fcf3697d7688769180f")
import time

API_TOKEN = '8046JRKkFhvlD1xAYc'

user_steps = dict()    # {cid: step, ...}
user_data = dict()     # {cid: {'first_name': str, 'last_name': str}, ...}

hideboard = ReplyKeyboardRemove()

bot = telebot.TeleBot(API_TOKEN, num_threads=10)

commands = {
    'start'             :   'start the bot',
    'help'              :   'show help menu',
    'get_info'          :   'get user information',
    'get_keyboard'      :   'show sample keyboard',
}

# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        # print(m)
        if m.content_type == 'text':
            print(f"{m.chat.first_name} [{m.chat.id}]: {m.text}")


bot.set_update_listener(listener)  # register listener


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

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()