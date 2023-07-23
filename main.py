import telebot

from config import bot_api,currency_api
import requests
from telebot import types
from currency_converter import CurrencyConverter

bot = telebot.TeleBot(bot_api)
currency = CurrencyConverter()
amount = 0
url = f'https://v6.exchangerate-api.com/v6/{currency_api}/latest/USD'
req = requests.get(url)
data = req.json()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id ,'ПРИВЕТ,введите сумму')
    bot.register_next_step_handler(message,summa)

def summa(message):
    global amount
    try :
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! НЕ правильно ввели сумму')
        bot.register_next_step_handler(message,summa)
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('USD/EUR',callback_data= 'usd/eur')
    btn2 = types.InlineKeyboardButton('EUR/USD',callback_data='eur/usd')
    btn3 = types.InlineKeyboardButton('USD/KZT',callback_data='usd/kzt')
    btn4 = types.InlineKeyboardButton('KZT/USD',callback_data='kzt/usd')
    markup.add(btn1,btn2,btn3,btn4)
    bot.send_message(message.chat.id,'Выберите пару валют',reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    values = call.data.upper().split('/')
    usd = data['conversion_rates']['USD']
    kzt = data['conversion_rates']['KZT']
    try:
        if values[0] == 'USD' and values[1] == 'EUR':
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(call.message.chat.id, f'Получается: {res}€. ')
        elif values[0] == 'EUR' and values[1] == 'USD':
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(call.message.chat.id, f'Получается: {res}$. ')
        if values[0] == 'USD' and values[1] == 'KZT':
            bot.send_message(call.message.chat.id, f'Получается: {amount * kzt}₸. ')
        elif values[0] == 'KZT' and values[1] == 'USD':
            bot.send_message(call.message.chat.id, f'Получается: {amount / kzt}$. ')
    except Exception:
        bot.send_message(call.message.chat.id,'Что-то не таак.Впишите значение заново')
        
bot.polling(none_stop=True)
