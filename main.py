import telebot
from telebot import types
token = '5501044032:AAGfy4Lg7ZwRxOngtQS89cKRmkBJ-KyPuns'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, напиши слово "Начать" для старта')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Начать":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Покажи лидерборд Топ-5 акций")
        item2 = types.KeyboardButton("Подробная аналитика по акциям")
        item3 = types.KeyboardButton("Прогноз для акции")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, 'Выберите, что вы хотите сделать', reply_markup=markup)
    elif message.text == "Покажи лидерборд Топ-5 акций":
        bot.send_message(message.chat.id, 'тут будет лидерборд:)) ')
    elif message.text == "Подробная аналитика по акциям":
        bot.send_message(message.chat.id, 'тут будет зарашиваться акция и потом ее аналитика:)) ')
    elif message.text == "Прогноз для акции":
        bot.send_message(message.chat.id, 'тут будет зарашиваться акция и потом ее прогноз:)) ')
    else:
        bot.send_message(message.chat.id, 'к сожалению, на это я ещё не научился отвечать, но я работаю над этим:( ')


bot.infinity_polling()
