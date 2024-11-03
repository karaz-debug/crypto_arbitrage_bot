# scripts/exchanges.py
## initialize connections to the exchanges.

import ccxt
from config import API_KEYS

def initialize_exchanges():
    exchanges = {}
    for exchange_name, credentials in API_KEYS.items():
        try:
            exchange_class = getattr(ccxt, exchange_name)
            exchange = exchange_class({
                'apiKey': credentials['api_key'],
                'secret': credentials['secret'],
                'enableRateLimit': True,
            })
            # Load markets to validate connection
            exchange.load_markets()
            exchanges[exchange_name] = exchange
            print(f"Connected to {exchange_name}")
        except AttributeError:
            print(f"Exchange {exchange_name} is not supported by ccxt.")
        except Exception as e:
            print(f"Failed to connect to {exchange_name}: {e}")
    return exchanges
