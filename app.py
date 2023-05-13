import telebot
import yahoo_parser as parser
import pandas as pd
from tabulate import tabulate


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
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.send_message(message.chat.id,
                                  'Привет, Акционер! Давай познакомимся поближе - напиши команду /help',
                                  reply_markup=self.keyboard)

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
                self.bot.send_message(message.chat.id, 'Введите название акции, на которую оформляете подписки')
                self.bot.register_next_step_handler(message, subscribe)  # переход к след действию

            elif message.text == 'Отписаться':
                self.bot.send_message(message.chat.id, 'Введите название акции,от которой хотите отписаться')
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
                self.bot.register_next_step_handler(message, read_share)  # переход к след действию

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
                self.bot.send_message(message.chat.id, 'Введите название акции и её количество')
                self.bot.register_next_step_handler(message, add_share)

            elif message.text == 'Удалить акцию':
                #TODO smrgn
                # по аналогии с методом Добавления: добавить метод-обработчик remove_share
                # в нем точно так же спросить имя акции (но уже без количества)
                # триггернуть метод БД remove_share(param=share_nm)
                # обработать ответ от БД (bool)
                # if successful:
                #   отправь пользователю: удаление успешно
                self.bot.send_message(message.chat.id, 'Введите название акции')
                self.bot.register_next_step_handler(message, remove_share)

            elif message.text == 'Изменить количество':
                #TODO smrgn
                # делать так же как предыдущие 2 метода, считывать в новом методе имя акции + новое актуальное значение кол-ва
                # считывай одним сообщение с помощью input.split
                # проверяй, что кол-во ввел целочисленное + положительное (если 0, скажи, что надо в функционал Удаление)
                # триггерни метод БД update_share(param=share_nm, amount)
                # получи ответ от БД (bool) Об успешности операции
                self.bot.send_message(message.chat.id, 'Введите название акции и актуальное количество')
                self.bot.register_next_step_handler(message, update_share)

            elif message.text == 'Мои акции':
                # получаем данные о портфеле из базы данных
                portfolio_data = self.db.get_portfolio()

                # если это не датафрейм просим пользователя сначала добавить акции в портфель
                if not isinstance(portfolio_data, pd.DataFrame):
                    self.bot.send_message(message.chat.id, 'Для удобного отображения вашего портфеля акций сначала '
                                                           'заполните информацию о нём')
                else:
                    table = tabulate(portfolio_data, headers='keys', tablefmt='orgtbl', showindex=False)
                    self.bot.send_message(message.chat.id, f'Список ваших акций:\n<pre>{table}</pre>',
                                          parse_mode='HTML', reply_markup=self.nested_keyboard_3)

            else:
                # Отправляем сообщение и клавиатуру с основными кнопками
                self.bot.send_message(message.chat.id,
                                      'Я еще не научился читать мысли, а такой команды не знаю :('
                                      '\nВозможно, тебе стоит заглянуть в /help',
                                      reply_markup=self.keyboard)

        def read_share(message):
            share_nm = message.text.lower()
            pic = parser.search_by_name(share_nm)
            if pic is not None:
                self.bot.send_photo(message.chat.id, pic)
            else:
                self.bot.send_message(message.chat.id, 'Такой акции нет :(')

        def subscribe(message):
            share_nm = message.text.lower()

            if self.db.sub_exists(message.chat.id, share_nm):
                self.bot.send_message(message.chat.id, 'У тебя уже есть подписка на эту акцию')
            else:
                share_found = parser.share_exists(share_nm)
                share_found = True
                if not share_found:
                    self.bot.send_message(message.chat.id, 'Такой акции нет :(')
                else:
                    self.bot.send_message(message.chat.id, 'Выберите время рассылки',
                                          reply_markup=self.time_keyboard)
                    self.bot.register_next_step_handler(message, subscribe_next, share_nm)

        def unsubscribe(message):
            share_nm = message.text.lower()

            if not self.db.sub_exists(message.chat.id, share_nm):
                self.bot.send_message(message.chat.id, 'У тебя нет подписки на эту акцию')
            else:
                self.db.unsubscribe(message.chat.id, share_nm)
                self.bot.send_message(message.chat.id, 'Вы успешно отписались',
                                      reply_markup=self.nested_keyboard_2)

        def subscribe_next(message, share_nm):
            chat_id = message.chat.id

            if message.text == '10:00' or message.text == '14:00' or message.text == '18:00' or message.text == '22:00':
                delivery_tm = message.text
                self.db.sub_add(chat_id, share_nm, delivery_tm)
                self.bot.send_message(message.chat.id, 'Вы успешно подписались!',
                                      reply_markup=self.keyboard)
            else:
                self.bot.send_message(message.chat.id, 'Некорректное время',
                                      reply_markup=self.nested_keyboard_2)

        def add_share(message): #меня смущает, что название такое же как и в файле database
            share_nm, amount = message.text.split()
            #while int(amount) <= 0:
            #    self.bot.send_message(message.chat.id,'Количество акций должно быть больше 0, введите корректное количество акций')
            #    amount = message.text так не работает, потому что он берет старое значение месседж(( пока не придумала, как пофиксить
            if parser.share_exists(share_nm) and (int(amount) > 0):
                if db.Database.add_share(message.chat.id, share_nm, int(amount)): #c параметрами тут косяк явный
                    self.bot.send_message(message.chat.id, 'Акция успешно записана:)')
            #TODO smrgn
            # дописать обработку случаев, когда акции нет и/или количество меньше 0
            # а также случай, когда акция не записалась в базу данных, но я, честно говоря, не очень понимаю, как это обработать

        def remove_share(message):
            share_nm = message.text
            # проверка, что такая акция есть в протфеле
            if db.Database.remove_share(message.chat.id, share_nm): #c параметрами тут косяк явный
                self.bot.send_message(message.chat.id, 'Акция успешно удалена:)')

        def update_share(message):
            share_nm, amount = message.text.split()
            if int(amount) == 0:
                self.bot.send_message(message.chat.id, 'Вероятно, вам следует использовать кнопку "Удалить акцию"')
            # if тоже проверка, что такая акция есть в портфеле and (int(amount) > 0):
            if db.Database.update_share(message.chat.id, share_nm, amount):
                self.bot.send_message(message.chat.id, 'Количество успешно обновлено')
        #TODO smrgn
        # Ну аналогично предыдущем функциям, реализовать в случае, когда не успешно что-то
        # + я не сделала проверку на целочисленное, а тупо беру целую часть, тоже не очень решение, подумаю, как пофиксить
        # пока пушу так, я их не могу тестить, так как функции, которые использую, или не реализованы, или реализованы иначе

    def start(self):  # метод, срабатывающий при запуске бота
        print('============= BOT START ===============')
        print('Bot is starting...')
        self.bot.infinity_polling()
        print('============= BOT STOP ===============')
