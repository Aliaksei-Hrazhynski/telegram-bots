import telebot
import sqlite3
import random
from telebot import types

bot = telebot.TeleBot('5690327160:AAFdC-siS8IqCO2OBxVKt5ivQAXnIwuSEX8')
conn = sqlite3.connect('db/dc_by.db', check_same_thread=False)
cursor = conn.cursor()


def get_toast():
    n_toast = random.randint(1, len(cursor.execute("""SELECT * from toasts""").fetchall()))
    sqlite_select_query = f"""SELECT * from toasts where id = {n_toast}"""
    cursor.execute(sqlite_select_query)
    record = cursor.fetchone()
    return record[1]

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['toast'])
def toast(message):
    mess = get_toast()
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    toast = types.KeyboardButton('/toast')
    markup.add(toast)
    bot.send_message(message.chat.id, 'Нажмите на кнопку с командой', reply_markup=markup)

bot.polling(none_stop=True)
