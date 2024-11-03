# scripts/report.py

import pandas as pd

def generate_report(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()

    trades = []
    for line in lines:
        if 'Arbitrage trade executed successfully' in line:
            parts = line.split(' - ')
            timestamp = parts[0]
            message = parts[-1]
            trades.append({'timestamp': timestamp, 'details': message})

    df = pd.DataFrame(trades)
    print(df)

if __name__ == "__main__":
    generate_report('../data/arbitrage_bot.log')
