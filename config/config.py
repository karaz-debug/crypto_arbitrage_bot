##  Contains configuration files such as API keys and settings.
# scripts/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../config/.env')

API_KEYS = {
    'binance': {
        'api_key': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_SECRET_KEY'),
    },
    'kraken': {
        'api_key': os.getenv('KRAKEN_API_KEY'),
        'secret': os.getenv('KRAKEN_SECRET_KEY'),
    },
    # Add more exchanges as needed
}

TRANSACTION_FEES = {
    'binance': float(os.getenv('BINANCE_FEE', 0.001)),
    'kraken': float(os.getenv('KRAKEN_FEE', 0.002)),
    # Add more as needed
}

SYMBOL = os.getenv('SYMBOL', 'BTC/USD')
MIN_PROFIT = float(os.getenv('MIN_PROFIT', 10))  # Minimum profit in USD
TRADE_AMOUNT = float(os.getenv('TRADE_AMOUNT', 0.001))  # Amount of BTC to trade

