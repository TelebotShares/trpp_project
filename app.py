import telebot
import schedule
import yahoo_parser as parser
import pandas as pd
from tabulate import tabulate
import threading
import time


def start_scheduler():
    """
        Starts scheduler for subscriptions delivery.
    """
    while True:
        schedule.run_pending()
        time.sleep(1*60)


# Класс, реализующий функционал бота
class TelebotShares:
    """
        Class with bot functionality.
    """

    def __init__(self, token, db):  # инициализация
        """
        Bot constructor - sets up bot, adds handlers.
        :param str token: bot token,
        :param db: database object
        """

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
        self.nested_keyboard_1.add(self.nested_button11, self.return_button)

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

        # Выбор времени (функционал Подписок)
        self.time_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        self.timebutton_1 = telebot.types.KeyboardButton('10:00')
        self.timebutton_2 = telebot.types.KeyboardButton('14:00')
        self.timebutton_3 = telebot.types.KeyboardButton('18:00')
        self.timebutton_4 = telebot.types.KeyboardButton('22:00')

        self.time_keyboard.add(self.timebutton_1, self.timebutton_2,
                               self.timebutton_3, self.timebutton_4)

        self.add_handlers()  # Добавляет обработчики сообщений
        print('Bot is set up')

    def add_handlers(self):  # обработчики сообщений
        """
        Adds message handlers to bot.
        """
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            """
            /start command handler.

            :param message: user message
            :rtype: None
            """
            self.bot.send_message(message.chat.id,
                                  'Привет, Акционер! Давай познакомимся поближе - напиши команду /help',
                                  reply_markup=self.keyboard)

            # register new user
            chat_id = message.chat.id
            self.db.reg_user(chat_id)

        @self.bot.message_handler(commands=['help'])  # просто текстовая команда
        def send_help(message):
            """
            /help command handler

            :param message: user message
            :rtype: None
            """
            self.bot.send_message(message.chat.id,
                                  'Сейчас я кратко расскажу о своих возможностях и как нам общаться, чтобы понимать '
                                  'друг друга &#128522\n\nОколо клавиатуры ты можешь найти кнопки, в основном мы будем '
                                  'общаться через них :)\n\nЕсли тебе нужна помощь по кнопкам, нажми или набери '
                                  'команду для\nкнопки «Биржа» /market\nкнопки «Подписки» /subscriptions\n'
                                  'кнопки «Мой портфель» /portfolio\n\n<i>Часто возникающая проблемка:</i>\n<b>«Я пишу '
                                  'акцию Apple, а бот отвечает, что такой акции нет, как такое возможно?»</b>\n\n'
                                  'Мы парсим данные с сайта "Yahoo Finance", поэтому, когда я прошу написать название '
                                  'акции, я имею в виду её код :)\n\nВот несколько примеров\n'
                                  '&#10060 Apple = AAPL &#9989\n&#10060 Papa John\'s = PZZA &#9989\n&#10060 '
                                  'Microsoft = MSFT &#9989\n\nКоды для других акций ты можешь найти по ссылке:\n'
                                  '<i>скоро тут будет ссылка</i>', parse_mode='html')

        @self.bot.message_handler(commands=['market'])
        def send_market(message):
            self.bot.send_message(message.chat.id, '<b>Кнопка «Биржа»</b>\n• Здесь ты можешь найти краткую '
                                                   'сводку по актуальной ситуации на бирже. Я попрошу тебя ввести '
                                                   'название акции, после чего верну статистику &#128200',
                                  parse_mode='html')

        @self.bot.message_handler(commands=['portfolio'])
        def send_portfolio(message):
            self.bot.send_message(message.chat.id, '<b>Кнопка «Мой портфель»</b>\n• Здесь ты можешь хранить свои акции,'
                                                   ' чтобы всегда помнить, какие акции у тебя есть и в каком '
                                                   'количествe &#128188\n<b>(Важно!)</b> Когда я прошу указать '
                                                   'название акции и её количество, формат ввода:\n“aapl 10” '
                                                   '(название, пробел, количество, без кавычек)', parse_mode='html')

        @self.bot.message_handler(commands=['subscriptions'])
        def send_subscriptions(message):
            self.bot.send_message(message.chat.id, '<b>Кнопка «Подписки»</b>\n• Здесь ты можешь '
                                                   'подписаться на рассылку актуальной цены по акциям &#129321 '
                                                   'Для того чтобы это сделать просто следуй моим указаниям :)\nТакже '
                                                   'ты можешь проверить свои подписки и отписаться, если какие-то '
                                                   'перестали быть тебе интересны.\n<b>(Важно!)</b> Если ты хочешь '
                                                   'изменить время рассылки, тебе необходимо отписаться и оформить '
                                                   'подписку заново', parse_mode='html')

        # Обрабатываем нажатие кнопок
        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            """
            All interactions with user with keyboard.

            :param message: user message
            :rtype: None
            """
            # взаимодействие с клавиатурой
            if message.text == 'Биржа':
                # Отправляем сообщение и клавиатуру с вложенными кнопками
                self.bot.send_message(message.chat.id, 'Вы перешли в раздел "Биржа"', reply_markup=self.nested_keyboard_1)
            elif message.text == 'Подписки':
                # Отправляем сообщение и клавиатуру с вложенными кнопками
                self.bot.send_message(message.chat.id, 'Вы перешли в раздел "Подписки"',
                                      reply_markup=self.nested_keyboard_2)
            elif message.text == 'Мой портфель':
                # Отправляем сообщение и клавиатуру с вложенными кнопками
                self.bot.send_message(message.chat.id, 'Вы перешли в раздел "Мой портфель"',
                                      reply_markup=self.nested_keyboard_3)
            elif message.text == 'Назад':
                self.bot.send_message(message.chat.id, 'Вы вернулись на главный экран',
                                      reply_markup=self.keyboard)

            # блок подписок
            elif message.text == 'Подписаться':
                self.bot.send_message(message.chat.id, 'Введите название акции, на которую хотите оформить подписку')
                self.bot.register_next_step_handler(message, subscribe)  # переход к след действию

            elif message.text == 'Отписаться':
                self.bot.send_message(message.chat.id, 'Введите название акции, от которой хотите отписаться')
                self.bot.register_next_step_handler(message, unsubscribe)  # переход к след действию

            elif message.text == 'Мои подписки':
                subs = self.db.get_subscriptions(message.chat.id)

                if not subs:
                    self.bot.send_message(message.chat.id, 'У вас нет подписок :(', reply_markup=self.nested_keyboard_2)
                else:
                    df = pd.DataFrame(subs, columns=['Акция', 'Время рассылки'])
                    df['Акция'] = df['Акция'].str.upper()
                    df['Время рассылки'] = pd.to_datetime(df['Время рассылки']).dt.strftime('%H:%M')
                    table = tabulate(df, headers='keys', tablefmt='orgtbl', showindex=False)
                    self.bot.send_message(message.chat.id, f'Список ваших подписок:\n<pre>{table}</pre>',
                                          parse_mode='HTML', reply_markup=self.nested_keyboard_2)

            # блок Биржи
            elif message.text == 'Поиск по акции':
                self.bot.send_message(message.chat.id, 'Введите название акции')
                self.bot.register_next_step_handler(message, share_stat)  # переход к след действию

            # блок Мой портфель
            elif message.text == 'Добавить акцию':
                self.bot.send_message(message.chat.id, 'Введите название акции, которую хотите добавить,'
                                                       ' и её количество')
                self.bot.register_next_step_handler(message, add_share)

            elif message.text == 'Удалить акцию':
                self.bot.send_message(message.chat.id, 'Введите название акции, которую хотите удалить')
                self.bot.register_next_step_handler(message, remove_share)

            elif message.text == 'Изменить количество':
                self.bot.send_message(message.chat.id, 'Введите название акции и актуальное количество')
                self.bot.register_next_step_handler(message, update_share)

            elif message.text == 'Мои акции':
                # получаем данные о портфеле из базы данных
                portfolio_data = self.db.get_portfolio(message.chat.id)

                # если это не датафрейм просим пользователя сначала добавить акции в портфель
                if not isinstance(portfolio_data, pd.DataFrame):
                    self.bot.send_message(message.chat.id, 'Для удобного отображения вашего портфеля акций сначала '
                                                           'заполните информацию о нём')
                else:
                    portfolio_data['Акция'] = portfolio_data['Акция'].str.upper()
                    table = tabulate(portfolio_data, headers='keys', tablefmt='orgtbl', showindex=False)
                    self.bot.send_message(message.chat.id, f'Список ваших акций:\n<pre>{table}</pre>',
                                          parse_mode='HTML', reply_markup=self.nested_keyboard_3)

            else:
                # Отправляем сообщение и клавиатуру с основными кнопками
                self.bot.send_message(message.chat.id,
                                      'Я еще не научился читать мысли, а такой команды не знаю :('
                                      '\nВозможно, тебе стоит заглянуть в /help',
                                      reply_markup=self.keyboard)

        def share_stat(message):
            """
            Sends share statistics to user.

            :param message: share name
            :rtype: None
            """
            share_nm = message.text.lower()
            pic = parser.search_by_name(share_nm)
            if pic is not None:
                self.bot.send_photo(message.chat.id, pic)
            else:
                self.bot.send_message(message.chat.id, 'Такой акции нет :(')

        def subscribe(message):
            """
            Starts adding subscription and checks for validness of operation.

            :param message: share name
            :rtype: None
            """
            share_nm = message.text.lower()

            if self.db.sub_exists(message.chat.id, share_nm):
                self.bot.send_message(message.chat.id, 'У тебя уже есть подписка на эту акцию :)')
            else:
                share_found = parser.share_exists(share_nm)
                if not share_found:
                    self.bot.send_message(message.chat.id, 'Такой акции нет :(')
                else:
                    self.bot.send_message(message.chat.id, 'Выберите время рассылки',
                                          reply_markup=self.time_keyboard)
                    self.bot.register_next_step_handler(message, subscribe_next, share_nm)

        def unsubscribe(message):
            """
            Removes subscription and checks for validness of operation.

            :param message: user message
            :rtype: None
            """
            share_nm = message.text.lower()

            if not self.db.sub_exists(message.chat.id, share_nm):
                self.bot.send_message(message.chat.id, 'У тебя нет подписки на эту акцию :(')
            else:
                self.db.unsubscribe(message.chat.id, share_nm)
                self.bot.send_message(message.chat.id, 'Вы успешно отписались!',
                                      reply_markup=self.nested_keyboard_2)

        def subscribe_next(message, share_nm):
            """
            Adds subscription and reads delivery time from user.

            :param message: user message
            :param str share_nm: share name
            :rtype: None
            """
            chat_id = message.chat.id

            if message.text == '10:00' or message.text == '14:00' or message.text == '18:00' or message.text == '22:00':
                delivery_tm = message.text
                self.db.sub_add(chat_id, share_nm, delivery_tm)
                self.bot.send_message(message.chat.id, 'Вы успешно подписались!',
                                      reply_markup=self.keyboard)
            else:
                self.bot.send_message(message.chat.id, 'Некорректное время',
                                      reply_markup=self.nested_keyboard_2)

        def add_share(message):
            """
            Adds share and checks for validness of operation.

            :param message: user message
            :rtype: None
            """
            # check message for 2 arguments
            space = True
            counter = 0
            for i in message.text:
                if i == ' ' or i == '\n' or i == '\t':
                    space = True
                elif space:
                    space = False
                    counter += 1

            if counter != 2:
                self.bot.send_message(message.chat.id, 'Необходимо вводить ровно 2 значения',
                                      reply_markup=self.nested_keyboard_3)
                return

            share_nm, amount = message.text.split()
            share_nm = share_nm.lower()
            if not amount.isdigit():
                self.bot.send_message(message.chat.id, 'Некорректное количество',
                                      reply_markup=self.nested_keyboard_3)
            elif not parser.share_exists(share_nm):
                self.bot.send_message(message.chat.id, 'Такой акции нет :(',
                                      reply_markup=self.nested_keyboard_3)
            else:
                added = self.db.add_share(message.chat.id, share_nm, int(amount))
                if not added:
                    self.bot.send_message(message.chat.id, 'Ты уже добавлял эту акцию :)',
                                          reply_markup=self.nested_keyboard_3)
                else:
                    self.bot.send_message(message.chat.id, 'Акция успешно добавлена!',
                                          reply_markup=self.nested_keyboard_3)

        def remove_share(message):
            """
            Removes share and check for validness of operation.

            :param message: user message
            :rtype: None
            """
            share_nm = message.text
            share_nm = share_nm.lower()
            removed = self.db.remove_share(message.chat.id, share_nm)

            if not removed:
                self.bot.send_message(message.chat.id, 'Ты не добавлял такую акцию :(')
            else:
                self.bot.send_message(message.chat.id, 'Акция успешно удалена!')

        def update_share(message):
            """
            Updates share amount and checks for validness of operation.

            :param message: user message
            :rtype: None
            """
            # check message for 2 arguments
            space = True
            counter = 0
            for i in message.text:
                if i == ' ' or i == '\n' or i == '\t':
                    space = True
                elif space:
                    space = False
                    counter += 1

            if counter != 2:
                self.bot.send_message(message.chat.id, 'Необходимо вводить ровно 2 значения',
                                      reply_markup=self.nested_keyboard_3)
                return

            share_nm, amount = message.text.split()
            share_nm = share_nm.lower()
            if amount == '0':
                self.bot.send_message(message.chat.id, 'Возможно, ты хочешь удалить акцию. '
                                                       'Для этого воспользуйся кнопкой "Удалить акцию"',
                                      reply_markup=self.nested_keyboard_3)
            elif not amount.isdigit():
                self.bot.send_message(message.chat.id, 'Некорректное количество',
                                      reply_markup=self.nested_keyboard_3)
            else:
                changed = self.db.update_share(message.chat.id, share_nm, int(amount))
                if not changed:
                    self.bot.send_message(message.chat.id, 'Ты не добавлял такую акцию :(',
                                          reply_markup=self.nested_keyboard_3)
                else:
                    self.bot.send_message(message.chat.id, 'Количетсво акций обновлено!',
                                          reply_markup=self.nested_keyboard_3)

    def send_subs_10(self):
        """
        Sends subs at 10:00.

        :rype: None
        """
        data = self.db.get_schedule('10:00')  # return chat_id + share_nm

        shares = pd.unique(data['share_nm'])
        shares_info = parser.actual_info(shares)  # return share_nm + price

        res = data.join(shares_info.set_index('share_nm'), on='share_nm')
        res = res.filter(items=['chat_id', 'share_nm', 'price'])
        res.rename(columns={'share_nm': 'Акция', 'price': 'Цена'}, inplace=True)

        chats = pd.unique(res['chat_id'])
        for chat in chats:
            sub = res[(res.chat_id == chat)]
            sub = sub.filter(items=['Акция', 'Цена'])
            table = tabulate(sub, headers='keys', tablefmt='orgtbl', showindex=False)
            self.bot.send_message(chat, f'Рассылка по вашей подписке:\n<pre>{table}</pre>',
                                  parse_mode='HTML')

    def send_subs_14(self):
        """
        Sends subs at 14:00.

        :rype: None
        """
        data = self.db.get_schedule('14:00')  # return chat_id + share_nm

        shares = pd.unique(data['share_nm'])
        shares_info = parser.actual_info(shares)  # return share_nm + price

        res = data.join(shares_info.set_index('share_nm'), on='share_nm')
        res = res.filter(items=['chat_id', 'share_nm', 'price'])
        res.rename(columns={'share_nm': 'Акция', 'price': 'Цена'}, inplace=True)

        chats = pd.unique(res['chat_id'])
        for chat in chats:
            sub = res[(res.chat_id == chat)]
            sub = sub.filter(items=['Акция', 'Цена'])
            table = tabulate(sub, headers='keys', tablefmt='orgtbl', showindex=False)
            self.bot.send_message(chat, f'Рассылка по вашей подписке:\n<pre>{table}</pre>',
                                  parse_mode='HTML')

    def send_subs_18(self):
        """
        Sends subs at 18:00.

        :rype: None
        """
        data = self.db.get_schedule('18:00')  # return chat_id + share_nm

        shares = pd.unique(data['share_nm'])
        shares_info = parser.actual_info(shares)  # return share_nm + price

        res = data.join(shares_info.set_index('share_nm'), on='share_nm')
        res = res.filter(items=['chat_id', 'share_nm', 'price'])
        res.rename(columns={'share_nm': 'Акция', 'price': 'Цена'}, inplace=True)

        chats = pd.unique(res['chat_id'])
        for chat in chats:
            sub = res[(res.chat_id == chat)]
            sub = sub.filter(items=['Акция', 'Цена'])
            table = tabulate(sub, headers='keys', tablefmt='orgtbl', showindex=False)
            self.bot.send_message(chat, f'Рассылка по вашей подписке:\n<pre>{table}</pre>',
                                  parse_mode='HTML')

    def send_subs_22(self):
        """
        Sends subs at 22:00.

        :rype: None
        """
        data = self.db.get_schedule('22:00')  # return chat_id + share_nm

        shares = pd.unique(data['share_nm'])
        shares_info = parser.actual_info(shares)  # return share_nm + price

        res = data.join(shares_info.set_index('share_nm'), on='share_nm')
        res = res.filter(items=['chat_id', 'share_nm', 'price'])
        res.rename(columns={'share_nm': 'Акция', 'price': 'Цена'}, inplace=True)

        chats = pd.unique(res['chat_id'])
        for chat in chats:
            sub = res[(res.chat_id == chat)]
            sub = sub.filter(items=['Акция', 'Цена'])
            table = tabulate(sub, headers='keys', tablefmt='orgtbl', showindex=False)
            self.bot.send_message(chat, f'Рассылка по вашей подписке:\n<pre>{table}</pre>',
                                  parse_mode='HTML')

    def start_planning(self):
        """
        Starts planning subscriptions delivery.

        :rtype: None
        """
        schedule.every().day.at('10:00').do(self.send_subs_10)
        schedule.every().day.at('14:00').do(self.send_subs_14)
        schedule.every().day.at('18:00').do(self.send_subs_18)
        schedule.every().day.at('22:00').do(self.send_subs_22)

    def start(self):  # метод, срабатывающий при запуске бота
        """
        Start the bot and runs the scheduler in separate thread.

        :rtype: None
        """
        print('============= BOT START ===============')
        print('Bot is starting...')
        # запуск планировщика
        scheduler_thread = threading.Thread(target=start_scheduler)
        scheduler_thread.start()

        # планирование рассылки
        self.start_planning()

        # запуск бота
        self.bot.infinity_polling()
        print('============= BOT STOP ===============')
