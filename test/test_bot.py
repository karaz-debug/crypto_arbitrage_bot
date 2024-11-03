## Contains test scripts for various components.
# tests/test_bot.py

import unittest
from unittest.mock import MagicMock
from data.arbitrage_bot import calculate_arbitrage_opportunities, select_best_opportunity

class TestArbitrage(unittest.TestCase):
    def setUp(self):
        # Sample price data
        self.prices_df = {
            'binance': {'bid': 50000, 'ask': 50100},
            'kraken': {'bid': 50200, 'ask': 50300},
            'coinbase': {'bid': 49900, 'ask': 50050},
        }

    def test_calculate_arbitrage_opportunities(self):
        import pandas as pd
        from data.arbitrage_bot import TRANSACTION_FEES, MIN_PROFIT

        prices_df = pd.DataFrame(self.prices_df).T
        opportunities = calculate_arbitrage_opportunities(prices_df)
        self.assertIsInstance(opportunities, list)
        # Check if at least one opportunity exists
        self.assertTrue(len(opportunities) >= 1)

    def test_select_best_opportunity(self):
        opportunities = [
            {'buy_exchange': 'binance', 'sell_exchange': 'kraken', 'net_profit': 20},
            {'buy_exchange': 'coinbase', 'sell_exchange': 'kraken', 'net_profit': 25},
        ]
        best = select_best_opportunity(opportunities)
        self.assertEqual(best['net_profit'], 25)

if __name__ == '__main__':
    unittest.main()
    
# pytest tests/test_bot.py

