import database
import app
from dotenv import load_dotenv
import os


load_dotenv()  # get credentials for environment


def main():  # функция main, запускающая бота
    """
        Running the  application.

        """
    db = database.Database()  # connect to DB
    bot = app.TelebotShares(os.environ['TOKEN'], db)  # init bot

    bot.start()  # start bot


if __name__ == '__main__':  # точка входа
    main()
