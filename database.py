import psycopg2
import pandas as pd
import os


class Database:
    """
    Database class
    """
    def __init__(self):
        """
        Database constructor
        """
        print('============= DATABASE CONNECT ===============')
        self.conn = psycopg2.connect(dbname=os.environ['DB_NAME'], user=os.environ['DB_USER'],
                                     password=os.environ['DB_PASS'], host=os.environ['DB_HOST'],
                                     port=os.environ['DB_PORT'])
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True
        print("Connected to DB")

    def test_query(self):
        """
            Testing communication with database.
        """
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

    def get_schedule(self, time):
        """
            Gets subscription delivery time from database

            :param str time: subscription delivery time
            :return: Table of chat ids and names of share to deliver
            :rtype: pd.DataFrame
        """
        time = time + ':00'
        sql = f'''
        select 
            t2.chat_id,
            t1.share_nm
        from subscription t1
            inner join tele_user t2
            on t1.user_id = t2.user_id
            and t1.delivery_tm = '{time}'::time;
        '''
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        res = pd.DataFrame(res, columns=['chat_id', 'share_nm'])
        return res

    def sub_add(self, chat_id, share_nm, delivery_tm):
        """
            Adds subscription to database.

            :param int chat_id: chat id
            :param str share_nm: share name
            :param str delivery_tm: subscription delivery_time
        """
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        uid = int(uid[0])
        delivery_tm = delivery_tm + ':00'
        sql = f'''
        insert into subscription 
        (user_id, share_nm, delivery_tm)
        values ({uid}, '{share_nm}', '{delivery_tm}'::time);
        '''
        self.cursor.execute(sql)

    def get_subscriptions(self, chat_id):
        """
            Get subscriptions from database.

            :param int chat_id: chat id
            :return: subscriptions info
            :rtype: list[tuple]
            """
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        uid = int(uid[0])

        sql = f'''select share_nm, delivery_tm::text from subscription
                where user_id = {uid}'''
        self.cursor.execute(sql)
        res = self.cursor.fetchall()

        return res

    def unsubscribe(self, chat_id, share_nm):
        """
            Removes subscription from database.

            :param int chat_id: chat id
            :param str share_nm: share name
        """
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        uid = int(uid[0])
        sql = f'''
        delete from subscription 
        where user_id = {uid} and share_nm = '{share_nm}';
        '''
        self.cursor.execute(sql)

    def sub_exists(self, chat_id, share_nm):
        """
            Checks if subscription exists in database.

            :param int chat_id: chat id
            :param str share_nm: share name
            :return: Existence of subscription
            :rtype: bool
            """
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        uid = int(uid[0])
        sql = f'''select sub_id from subscription where user_id = {uid} and share_nm = '{share_nm}';'''
        self.cursor.execute(sql)
        res = self.cursor.fetchone()

        if res:
            return True

        return False

    def add_share(self, chat_id, share_nm, amount):
        """
            Adds share to database.

            :param int chat_id: chat id
            :param str share_nm: share name
            :param int amount: amount of shares
            :return: Status of addition to database
            :rtype: bool
        """
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        uid = int(uid[0])
        sql = f'''select user_id, share_nm from user_x_share where user_id = {uid} and share_nm = '{share_nm}';'''
        self.cursor.execute(sql)
        res = self.cursor.fetchone()

        if res:
            return False

        sql = f'''
        insert into user_x_share
        (user_id, share_nm, amount) 
        values ({uid}, '{share_nm}', {amount});            
        '''
        self.cursor.execute(sql)

        return True

    def remove_share(self, chat_id, share_nm):
        """
            Removes share from database.

            :param int chat_id: chat id
            :param str share_nm: share_name
            :return: Status of removal from database.
            :rtype: bool
            """
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        uid = int(uid[0])
        sql = f'''select user_id, share_nm from user_x_share where user_id = {uid} and share_nm = '{share_nm}';'''
        self.cursor.execute(sql)
        res = self.cursor.fetchone()

        if not res:
            return False

        sql = f'''
                delete from user_x_share
                where user_id = {uid} and share_nm = '{share_nm}';            
                '''
        self.cursor.execute(sql)

        return True

    def update_share(self, chat_id, share_nm, amount):
        """
            Update share amount in database.

            :param int chat_id: chat id
            :param str share_nm: share name
            :param int amount: new amount of shares
            :return: Status of update in database.
            :rtype: bool
        """
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        uid = int(uid[0])
        print(uid)
        print(share_nm)
        sql = f'''select user_id, share_nm from user_x_share where user_id = {uid} and share_nm = '{share_nm}';'''
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        print(res)

        if not res:
            return False

        sql = f'''
                update user_x_share
                set amount = {amount}
                where user_id = {uid} and share_nm = '{share_nm}';            
                '''
        self.cursor.execute(sql)

        return True

    def get_portfolio(self, chat_id):
        """
            Return info about user's shares.

            :param int chat_id: chat id
            :return: Table with user's shares or unsuccessful status
            :rtype: str or pd.DataFrame
            """
        sql = f'select user_id from tele_user where chat_id = {chat_id};'
        self.cursor.execute(sql)
        uid = self.cursor.fetchone()

        uid = int(uid[0])
        sql = f'select share_nm, amount from user_x_share where user_id = {uid};'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()

        if not res:
            return 'Shares not added'

        df = pd.DataFrame(res, columns=['Акция', 'Количество'])
        return df

    def reg_user(self, chat_id):
        """
            Registrate user in database.

            :param int chat_id: chat id
        """
        sql = f'select chat_id from tele_user where chat_id = {chat_id}'
        self.cursor.execute(sql)
        user_try = self.cursor.fetchone()
        if not user_try:
            sql = f'insert into tele_user (chat_id) values({chat_id})'
            self.cursor.execute(sql)
