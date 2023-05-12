import psycopg2
import config as cf
import pandas as pd


class Database:
    def __init__(self):
        print('============= DATABASE CONNECT ===============')
        self.conn = psycopg2.connect(dbname=cf.DB_NAME, user=cf.DB_USER, password=cf.DB_PASS,
                                     host=cf.DB_HOST, port=cf.DB_PORT)
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True
        print("Connected to DB")

    def simple_query(self):
        sql = 'select * from tele_user'
        self.cursor.execute(sql)
        # # Fetching 1st row from the table
        # result = self.cursor.fetchone()
        # print(result)

        # Fetching 1st row from the table
        result = pd.DataFrame(self.cursor.fetchall())
        print(result)

    def add_share(self, share_nm, amount):
        #TODO rybrix
        # return bool (successful update)
        pass

    def remove_share(self, share_nm):
        #TODO rybrix
        # return bool (successful removal)
        # в этом методе проверять на наличие у пользователя такой акции
        pass

    def update_share(self, share_nm, amount):
        #TODO rybrix
        pass

    def get_portfolio(self):
        #TODO rybrix
        # вернуть табличку вида название акции - кол-во у пользователя
        pass

    def reg_user(self, chat_id):
        sql = f'select chat_id from tele_user where chat_id = {chat_id}'
        self.cursor.execute(sql)
        user_try = self.cursor.fetchone()
        if not user_try:
            sql = f'insert into tele_user (chat_id) values({chat_id})'
            self.cursor.execute(sql)

    def stop_db(self):
        print('============= DATABASE STOP ===============')
        self.cursor.close()
        print('Cursor is closed')
        self.conn.close()
        print('Connection is closed')
