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

    def test_query(self):
        sql = 'select * from tele_user;'
        self.cursor.execute(sql)
        # # Fetching 1st row from the table
        result = self.cursor.fetchall()
        print(result)
        df = pd.DataFrame(result, columns=['user_id', 'chat_id'])
        print(df)
        print(type(df))

        # Fetching 1st row from the table
        # result = pd.DataFrame(self.cursor.fetchall())
        # print(result)

    def add_share(self, chat_id, share_nm, amount):
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        if not uid:
            return 'Registration error'

        uid = int(uid[0])
        sql = f'select user_id, share_nm from user_x_share where user_id = {uid} and share_nm = {share_nm};'
        self.cursor.execute(sql)
        res = self.cursor.fetchone()

        if res:
            return 'Share already added'

        sql = f'''
        insert into user_x_share
        (user_id, share_nm, amount) 
        values ({uid}, {share_nm}, {amount});            
        '''
        self.cursor.execute(sql)

        return 'GOOD'

    def remove_share(self, chat_id, share_nm):
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        if not uid:
            return 'Registration error'

        uid = int(uid[0])
        sql = f'select user_id, share_nm from user_x_share where user_id = {uid} and share_nm = {share_nm};'
        self.cursor.execute(sql)
        res = self.cursor.fetchone()

        if not res:
            return 'Such share not added'

        sql = f'''
                delete from user_x_share
                where user_id = {uid} and share_nm = {share_nm};            
                '''
        self.cursor.execute(sql)

        return 'GOOD'

    def update_share(self, chat_id, share_nm, amount):
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        if not uid:
            return 'Registration error'

        uid = int(uid[0])
        sql = f'select user_id, share_nm from user_x_share where user_id = {uid} and share_nm = {share_nm};'
        self.cursor.execute(sql)
        res = self.cursor.fetchone()

        if not res:
            return 'Such share not added'

        sql = f'''
                update user_x_share
                set amount = {amount}
                where user_id = {uid} and share_nm = {share_nm};            
                '''
        self.cursor.execute(sql)

        return 'GOOD'

    def get_portfolio(self, chat_id):
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        if not uid:
            return 'Registration error'

        uid = int(uid[0])
        sql = f'select share_nm, amount from user_x_share where user_id = {uid};'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()

        if not res:
            return 'Shares not added'

        df = pd.DataFrame(res, columns=['share_nm', 'amount'])
        return df

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