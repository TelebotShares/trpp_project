import pandas as pd
import requests.exceptions
import yfinance as yf
import io
from plotly.subplots import make_subplots
import plotly.graph_objects as go


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

    # get historical market data

    hist = share.history(period="1y", actions=False)
    if not hist.empty:
        hist['Datetime'] = hist.index
        hist['Datetime'] = hist['Datetime'].dt.tz_convert('Europe/Moscow')
        hist['Datetime'] = hist['Datetime'].dt.strftime("%m/%Y")

        hist['diff'] = hist['Close'] - hist['Open']
        hist.loc[hist['diff'] >= 0, 'color'] = 'green'
        hist.loc[hist['diff'] < 0, 'color'] = 'red'

        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(go.Candlestick(x=hist.index,
                                      open=hist['Open'],
                                      high=hist['High'],
                                      low=hist['Low'],
                                      close=hist['Close'],
                                      name='Price'))
        fig3.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(window=20).mean(),
                                  name='20 Day MA', marker_color='blue'))
        fig3.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker={'color': hist['color']}),
                       secondary_y=True)
        fig3.update_yaxes(range=[0, 700000000], secondary_y=True)
        fig3.update_yaxes(visible=False, secondary_y=True)
        fig3.update_layout(xaxis_rangeslider_visible=False)  # hide range slider
        fig3.update_layout(title={'text': name.upper(), 'x': 0.5})

        # save to buffer
        buf = io.BytesIO()
        fig3.write_image(buf, format='png')
        buf.seek(0)
        return buf
    return


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
