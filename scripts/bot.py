# scripts/bot.py

import time
from exchanges import initialize_exchanges
from data_fetcher import fetch_tickers, get_latest_prices
from data.arbitrage_bot import calculate_arbitrage_opportunities, select_best_opportunity
from executor import execute_trade
from logger import setup_logger
from  config import SYMBOL

logger = setup_logger()

def main():
    exchanges = initialize_exchanges()
    if not exchanges:
        logger.error("No exchanges connected. Exiting.")
        return

    while True:
        try:
            # Fetch latest tickers
            tickers = fetch_tickers(exchanges, SYMBOL)
            if not tickers:
                logger.warning("No tickers fetched. Skipping this cycle.")
                time.sleep(5)
                continue

            # Get latest prices as DataFrame
            prices_df = get_latest_prices(tickers)

            # Calculate arbitrage opportunities
            opportunities = calculate_arbitrage_opportunities(prices_df)

            if not opportunities:
                logger.info("No arbitrage opportunities found.")
            else:
                # Select the best opportunity
                best_opportunity = select_best_opportunity(opportunities)
                if best_opportunity:
                    # Execute the trade
                    buy_order, sell_order = execute_trade(best_opportunity, exchanges)
                    if buy_order and sell_order:
                        logger.info(f"Arbitrage trade executed successfully: {best_opportunity}")
                    else:
                        logger.error("Trade execution failed.")
            
            # Wait before next cycle
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info("Bot stopped by user.")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()


# Explanation:

# Initializes exchange connections.
# Enters an infinite loop to continuously monitor for arbitrage opportunities.
# For each cycle:
# Fetches the latest ticker data.
# Identifies arbitrage opportunities.
# Executes the most profitable trade.
# Waits for a specified interval before the next cycle.
# Handles graceful shutdown on user interruption and logs unexpected errors.