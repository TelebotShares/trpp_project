import telebot
import yahoo_parser as parser
import pandas as pd


# Класс, реализующий функционал бота
class TelebotShares:
    def __init__(self, token, db):  # инициализация
        print('============= BOT SET UP ===============')
        self.bot = telebot.TeleBot(token=token)
        self.db = db

        # Main keyboard
        self.keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        self.button1 = telebot.types.KeyboardButton('Биржа')
        self.button2 = telebot.types.KeyboardButton('Подписки')
        self.button3 = telebot.types.KeyboardButton('Мой портфель')
        self.keyboard.add(self.button1, self.button2, self.button3)

        self.return_button = telebot.types.KeyboardButton('Назад')

        # Кнопка Биржа
        self.nested_keyboard_1 = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        self.nested_button11 = telebot.types.KeyboardButton('Поиск по акции')
        self.nested_button12 = telebot.types.KeyboardButton('Лидерборд')
        self.nested_keyboard_1.add(self.nested_button11, self.nested_button12, self.return_button)

        # Кнопка Подписки
        self.nested_keyboard_2 = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        self.nested_button21 = telebot.types.KeyboardButton('Подписаться')
        self.nested_button22 = telebot.types.KeyboardButton('Отписаться')
        self.nested_button23 = telebot.types.KeyboardButton('Мои подписки')
        self.nested_keyboard_2.add(self.nested_button21, self.nested_button22, self.nested_button23,
                                   self.return_button)

        # Кнопка Мой портфель
        self.nested_keyboard_3 = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        self.nested_button31 = telebot.types.KeyboardButton('Добавить акцию')
        self.nested_button32 = telebot.types.KeyboardButton('Удалить акцию')
        self.nested_button33 = telebot.types.KeyboardButton('Изменить количество')
        self.nested_button34 = telebot.types.KeyboardButton('Мои акции')

        self.nested_keyboard_3.add(self.nested_button31, self.nested_button32, self.nested_button33,
                                   self.nested_button34, self.return_button)

        self.add_handlers()  # Добавляет обработчики сообщений
        print('Bot is set up')

    def add_handlers(self):  # обработчики сообщений
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.send_message(message.chat.id,
                                  'Привет, Акционер! Давай познакомимся поближе - напиши команду /help')

            # register new user
            chat_id = message.chat.id
            self.db.reg_user(chat_id)

        @self.bot.message_handler(commands=['help'])  # просто текстовая команда
        def send_help(message):
            self.bot.send_message(message.chat.id,
                                  'Здесь будет мое CV. Или можем узнать друг друга поближе в Тиндере.')
            #TODO smrgn
            # допиши тут в хелпе красиво про функционал кратко плз (и про то, за что отвечают блоки наши)

        # Обрабатываем нажатие кнопок
        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            # взаимодействие с клавиатурой
            if message.text == 'Биржа':
                # Отправляем сообщение и клавиатуру с вложенными кнопками
                self.bot.send_message(message.chat.id, 'Вы перешли в раздел Биржи', reply_markup=self.nested_keyboard_1)
            elif message.text == 'Подписки':
                # Отправляем сообщение и клавиатуру с вложенными кнопками
                self.bot.send_message(message.chat.id, 'Вы перешли в раздел Подписок',
                                      reply_markup=self.nested_keyboard_2)
            elif message.text == 'Мой портфель':
                # Отправляем сообщение и клавиатуру с вложенными кнопками
                self.bot.send_message(message.chat.id, 'Вы перешли в раздел Мой портфель',
                                      reply_markup=self.nested_keyboard_3)
            elif message.text == 'Назад':
                self.bot.send_message(message.chat.id, 'Вы вернулись на главный экран',
                                      reply_markup=self.keyboard)

            # блок подписок
            elif message.text == 'Подписаться':
                # TODO rybrix
                pass
            elif message.text == 'Отписаться':
                # TODO rybrix
                pass
            elif message.text == 'Мои подписки':
                # TODO rybrix
                pass

            # блок Биржи
            elif message.text == 'Поиск по акции':
                self.bot.send_message(message.chat.id, 'Введите название акции')
                self.bot.register_next_step_handler(message, read_share)  # переход к след действию

            elif message.text == 'Лидерборд':
                #TODO Qater
                # отсюда триггерить метод yahoo_parser для лидерборда
                # метод возвращает табличку датафрейм
                # придумать, как выводить лидерборд (табличку)
                pass

            # блок Мой портфель
            elif message.text == 'Добавить акцию':
                #TODO smrgn
                # send message to user 'write the name of your share (space) amount' (read by split, add check for amount: int, >0)
                # add register_next_step_handler: add_share (для примера посмотри read_share и откуда он вызывается)
                # in add_share get the share name
                # execute method from yahoo_parser.py (share_exists) with param=share_name (from user)
                # check for existance (the response of method share_exists())
                # if exists:
                #   trigger database.py method (add_share()) with param=share_name, amount
                #   get response from add_share()
                # if successful: send to user 'your share written successfully'
                pass
            elif message.text == 'Удалить акцию':
                #TODO smrgn
                # по аналогии с методом Добавления: добавить метод-обработчик remove_share
                # в нем точно так же спросить имя акции (но уже без количества)
                # триггернуть метод БД remove_share(param=share_nm)
                # обработать ответ от БД (bool)
                # if successful:
                #   отправь пользователю: удаление успешно
                pass
            elif message.text == 'Изменить количество':
                #TODO smrgn
                # делать так же как предыдущие 2 метода, считывать в новом методе имя акции + новое актуальное значение кол-ва
                # считывай одним сообщение с помощью input.split
                # проверяй, что кол-во ввел целочисленное + положительное (если 0, скажи, что надо в функционал Удаление)
                # триггерни метод БД update_share(param=share_nm, amount)
                # получи ответ от БД (bool) Об успешности операции
                pass
            elif message.text == 'Мои акции':
                #TODO Qater
                # смысл этого блока: вывести пользователю табличку вида (имя акции - кол-во у пользователя)
                # потом мб добавим статистику по портфелю (рост сбержеений или тому подобного, но пока Похуй+поебать)
                # триггерни метод БД get_portfolio (он вернет dataframe)
                # пользователю в чате вывести табличку (опять же, понять в каком виде)
                pass

            else:
                # Отправляем сообщение и клавиатуру с основными кнопками
                self.bot.send_message(message.chat.id,
                                      'Я еще не научился читать мысли, а такой команды не знаю :('
                                      '\nВозможно, тебе стоит заглянуть в /help',
                                      reply_markup=self.keyboard)

        def read_share(message):
            share_nm = message.text
            pic = parser.search_by_name(share_nm)
            if pic is not None:
                self.bot.send_photo(message.chat.id, pic)
            else:
                self.bot.send_message(message.chat.id, 'Такой акции нет :(')

    def start(self):  # метод, срабатывающий при запуске бота
        print('============= BOT START ===============')
        print('Bot is starting...')
        self.bot.infinity_polling()
        print('============= BOT STOP ===============')
