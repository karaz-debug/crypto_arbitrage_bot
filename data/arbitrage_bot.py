# scripts/arbitrage.py

import pandas as pd
from config import TRANSACTION_FEES, MIN_PROFIT, TRADE_AMOUNT, SYMBOL
from scripts.logger import setup_logger

logger = setup_logger()

def calculate_arbitrage_opportunities(prices_df):
    opportunities = []
    exchanges = prices_df.index.tolist()
    for i in range(len(exchanges)):
        for j in range(len(exchanges)):
            if i == j:
                continue
            buy_exchange = exchanges[i]
            sell_exchange = exchanges[j]
            buy_price = prices_df.at[buy_exchange, 'ask']
            sell_price = prices_df.at[sell_exchange, 'bid']
            fee_buy = TRANSACTION_FEES.get(buy_exchange, 0)
            fee_sell = TRANSACTION_FEES.get(sell_exchange, 0)
            net_profit = (sell_price * (1 - fee_sell)) - (buy_price * (1 + fee_buy))
            if net_profit > MIN_PROFIT:
                opportunities.append({
                    'buy_exchange': buy_exchange,
                    'sell_exchange': sell_exchange,
                    'buy_price': buy_price,
                    'sell_price': sell_price,
                    'net_profit': net_profit
                })
                logger.info(f"Arbitrage opportunity found: Buy {SYMBOL} on {buy_exchange} at {buy_price} and sell on {sell_exchange} at {sell_price} for profit {net_profit}")
    return opportunities

def select_best_opportunity(opportunities):
    if not opportunities:
        return None
    # Select the opportunity with the highest net profit
    best = max(opportunities, key=lambda x: x['net_profit'])
    logger.info(f"Best arbitrage opportunity: {best}")
    return best


# Explanation:

# calculate_arbitrage_opportunities: Iterates through all possible exchange pairs to identify
#profitable arbitrage opportunities after accounting for transaction fees.
# select_best_opportunity: Chooses the most profitable opportunity from the list.
