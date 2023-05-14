import pandas as pd
import requests.exceptions
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import io


def search_by_name(name):
  """
    Plots share history.

    :param str name: share name
    :return: Plot of share history
    :rtype: io.BytesIO or None
    """

    if not share_exists(name):
        return

    share = yf.Ticker(name)
    # get stock info
    # print(msft.info)

    # get historical market data

    intervals = ['30m', '1h', '2h', '4h', '8h', '1d']
    interval = '1d'
    for interval_temp in intervals:
        hist = share.history(period="5d", interval=interval_temp, actions=False)
        if not hist.empty:
            interval = interval_temp
            break
        elif interval_temp == '1d':
            return

    hist = share.history(period="5d", interval=interval, actions=False)

    hist['Datetime'] = hist.index
    hist['Datetime'] = hist['Datetime'].dt.tz_convert('Europe/Moscow')

    sns.set_style('whitegrid')
    plt.figure(figsize=(12, 6))
    plt.plot(hist['Datetime'], hist['Close'])
    plt.title = f'Цена на закрытии акции {name} за последние 5 дней'
    plt.xlabel = 'Дата, время'
    plt.ylabel = 'Цена, $'

    # save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def share_exists(share_nm):
    """
        Check for share existence.

        :param str share_nm: share name
        :return: Existence of share with such name
        :rtype: bool
        """
    share = yf.Ticker(share_nm.upper())

    try:
        # attempt to access info
        info = share.info

    # in case we could find such page
    except requests.exceptions.HTTPError:
        return False

    # if share exists and we got info about it
    return True


def actual_info(shares):
    """
        Gets the latest close price of shares.

        :param list[str] shares: names of shares
        :return: Table with shares and prices
        :rtype: pd.DataFrame
        """
    tickers = shares
    res = []
    for ticker in tickers:
        ticker_yahoo = yf.Ticker(ticker)
        data = ticker_yahoo.history()
        last_quote = data['Close'].iloc[-1]
        tup = (ticker, round(last_quote, 2))
        res.append(tup)
        print(ticker, last_quote)
    return pd.DataFrame(res, columns=['share_nm', 'price'])
