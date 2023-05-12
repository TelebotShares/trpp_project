from config import TOKEN
import database
import app


def main():  # функция main, запускающая бота
    db = database.Database()  # connect to DB
    bot = app.TelebotShares(TOKEN, db)  # init bot

    bot.start()  # start bot

    # when the bot is stopped
    db.stop_db()  # close connection to db


if __name__ == '__main__':  # точка входа
    main()
