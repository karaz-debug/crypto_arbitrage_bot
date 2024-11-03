# scripts/data_fetcher.py

import time
import pandas as pd
from exchanges import initialize_exchanges
from config import SYMBOL
from logger import setup_logger

logger = setup_logger()

# fetch_tickers: Fetches the ticker data for the specified symbol from each exchange.
def fetch_tickers(exchanges, symbol):
    tickers = {}
    for name, exchange in exchanges.items():
        try:
            ticker = exchange.fetch_ticker(symbol)
            tickers[name] = ticker
            logger.info(f"Fetched ticker from {name}: Bid={ticker['bid']}, Ask={ticker['ask']}")
        except Exception as e:
            logger.error(f"Error fetching ticker from {name}: {e}")
    return tickers

# tickers = {
#   'Binance': {'BTC/USD': {'bid': 50000, 'ask': 50100}},
#   'Coinbase': {'BTC/USD': {'bid': 50050, 'ask': 50150}}
# }

# get_latest_prices: Structures the fetched data into a pandas DataFrame for easier analysis.
def get_latest_prices(tickers):
    data = {}
    for exchange, ticker in tickers.items():
        data[exchange] = {
            'bid': ticker['bid'],
            'ask': ticker['ask'],
        }
    return pd.DataFrame(data).T

if __name__ == "__main__":
    exchanges = initialize_exchanges()
    while True:
        tickers = fetch_tickers(exchanges, SYMBOL)
        prices_df = get_latest_prices(tickers)
        print(prices_df)
        time.sleep(5)  # Fetch every 5 seconds
