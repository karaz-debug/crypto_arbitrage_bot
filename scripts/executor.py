# scripts/executor.py

# scripts/executor.py

import time
from config import TRADE_AMOUNT, SYMBOL
from logger import setup_logger

logger = setup_logger()

def execute_trade(opportunity, exchanges, max_retries=3, retry_delay=5):
    buy_exchange = exchanges[opportunity['buy_exchange']]
    sell_exchange = exchanges[opportunity['sell_exchange']]
    amount = TRADE_AMOUNT  # BTC to buy/sell

    for attempt in range(1, max_retries + 1):
        try:
            # Place buy order
            logger.info(f"Attempt {attempt}: Placing buy order on {opportunity['buy_exchange']} for {amount} {SYMBOL}")
            buy_order = buy_exchange.create_market_buy_order(SYMBOL, amount)
            logger.info(f"Buy order placed: {buy_order}")

            # Place sell order
            logger.info(f"Attempt {attempt}: Placing sell order on {opportunity['sell_exchange']} for {amount} {SYMBOL}")
            sell_order = sell_exchange.create_market_sell_order(SYMBOL, amount)
            logger.info(f"Sell order placed: {sell_order}")

            return buy_order, sell_order
        except Exception as e:
            logger.error(f"Error executing trades on attempt {attempt}: {e}")
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Trade execution failed.")
                return None, None

    
#execute_trade: Takes an arbitrage opportunity and executes a market buy order on the buy exchange and a market sell order on the sell exchange for the specified amount.
# Caution: Market orders can lead to slippage, especially in volatile markets. Consider using limit orders or implementing slippage protection.

# Implements a retry mechanism for trade executions.
# Waits for a specified delay before retrying in case of failures.
# Logs all attempts and errors.