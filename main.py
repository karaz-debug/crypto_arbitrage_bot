import ccxt
from config.config import API_KEYS
import logging

logging.basicConfig(
    filename='data/arbitrage_bot.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


## Create Exchange Instances
exchanges = {}
for exchange_name, credentials in API_KEYS.items():
    exchange_class = getattr(ccxt, exchange_name)
    exchanges[exchange_name] = exchange_class({
        'apiKey': credentials['api_key'],
        'secret': credentials['secret'],
        'enableRateLimit': True,
    })

## Fetch Tickers from Each Exchange:
def fetch_tickers(exchanges, symbols):
    tickers = {}
    for name, exchange in exchanges.items():
        try:
            ticker = exchange.fetch_ticker(symbols)
            tickers[name] = ticker
        except Exception as e:
            print(f"Error fetching ticker from {name}: {e}")
    return tickers

# tickers = {
#   'Binance': {'BTC/USD': {'bid': 50000, 'ask': 50100}},
#   'Coinbase': {'BTC/USD': {'bid': 50050, 'ask': 50150}}
# }

## Arbitrage Opportunity
def calculate_spread(tickers, symbol, fee_config):
    opportunities = []
    exchanges_list = list(tickers.keys())
    for i in range(len(exchanges_list)):
        for j in range(len(exchanges_list)):
            if i == j:
                continue
            buy_exchange = exchanges_list[i]
            sell_exchange = exchanges_list[j]
            buy_price = tickers[buy_exchange][symbol]['ask']
            sell_price = tickers[sell_exchange][symbol]['bid']
            fee_buy = fee_config[buy_exchange]
            fee_sell = fee_config[sell_exchange]
            net_profit = sell_price * (1 - fee_sell) - buy_price * (1 + fee_buy)
            if net_profit > 0:
                opportunities.append({
                    'buy_exchange': buy_exchange,
                    'sell_exchange': sell_exchange,
                    'buy_price': buy_price,
                    'sell_price': sell_price,
                    'net_profit': net_profit
                })
    return opportunities


# Developing Trade Execution Mechanism
def execute_arbitrage_opportunity(opportunity, amount):
    buy_exchange = exchanges[opportunity['buy_exchange']]
    sell_exchange = exchanges[opportunity['sell_exchange']]
    symbol = 'BTC/USD'  # Example symbol
    try:
        # Place buy order
        buy_order = buy_exchange.create_market_buy_order(symbol, amount)
        # Place sell order
        sell_order = sell_exchange.create_market_sell_order(symbol, amount)
        return buy_order, sell_order
    except Exception as e:
        print(f"Error executing trades: {e}")
        return None, None


