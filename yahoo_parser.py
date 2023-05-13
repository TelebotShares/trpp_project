import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import io


def search_by_name(name):
    share = yf.Ticker(name)
    # get stock info
    # print(msft.info)

    # get historical market data
    hist = share.history(period="5d", interval='30m', actions=False)

    if hist.empty:
        return

    sns.set_style('whitegrid')
    plt.figure(figsize=(12, 6))
    plt.plot(hist.index, hist['Close'])
    plt.title = f'Цена на закрытии акции {name} за последние 5 дней'
    plt.xlabel = 'Дата, время'
    plt.ylabel = 'Цена, $'

    # save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def share_exists(share_nm):
    share = yf.Ticker(share_nm.upper())
    hist = share.history(period="7d", interval='5d', actions=False)

    if hist.empty:
        return False

    return True
