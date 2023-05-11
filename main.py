import telebot
from telebot import types
import random
import pandas as pd
import yfinance as yf
from config import TOKEN


# Класс, реализующий функционал бота
class TelebotShares:
    def __init__(self, token):  # инициализация
        self.bot = telebot.TeleBot(token=token)
        self.add_handlers()  # Добавляет обработчики сообщений

    def add_handlers(self):  # обработчики сообщений
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.send_message(message.chat.id,
                                  'Привет, Акционер! Давай познакомимся поближе - напиши команду /help')
            self.send_buttons(message)

        @self.bot.message_handler(commands=['help']) # просто текстовая команда
        def send_help(message):
            self.bot.send_message(message.chat.id,
                                  'Здесь будет мое CV. Или можем узнать друг друга поближе в Тиндере.')

        @self.bot.message_handler(commands=['button']) # кнопка на клаве
        def button_message(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Начать")
            markup.add(item1)
            self.bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

        @self.bot.callback_query_handler(func=lambda call: True) # кнопки, привязанные к сообщению
        def handle_query(call):
            if call.data == 'random':
                random_number = random.randint(10, 20)
                self.bot.send_message(call.message.chat.id, f"Случайное число: {random_number}")
            elif call.data == 'parse':
                msft = yf.Ticker("MSFT")

                # get stock info
                print(msft.info)

                # get historical market data
                hist = msft.history(period="5d")
                print(hist)

                # 2nd way
                ticker = "MSFT"
                data = yf.download(ticker, start="2023-05-04", end="2023-05-11")

                # Выводим полученные данные
                print(data.head())

    def send_buttons(self, message):
        keyboard = telebot.types.InlineKeyboardMarkup()
        random_button = telebot.types.InlineKeyboardButton(text="Случайность", callback_data="random")
        parse_button = telebot.types.InlineKeyboardButton(text="Парсинг статистики", callback_data="parse")
        keyboard.row(random_button, parse_button)
        self.bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

    def start(self):  # метод, срабатывающий при запуске бота
        self.bot.infinity_polling()


def main():  # функция main, запускающая бота
    bot = TelebotShares(TOKEN)
    bot.start()


if __name__ == '__main__':  # точка входа
    main()
