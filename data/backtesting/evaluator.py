import pandas as pd
from datetime import datetime


def evaluate_graham():
    return



def evaluate_ml():
    transaction_history = ((pd.read_csv('data/backtesting/transaction_history_ml_50.csv')).sort_values(by=['entry_date'])) #.set_index('entry_date')
    pnl_percent_list = []
    holding_days_list = []

    for index, row in transaction_history.iterrows():
        pnl_percent_list.append(float((100 / row['entry_price'] * row['exit_price']) - 100))
        holding_days_list.append(int(row['holding_days'].replace(' days', '')))

    # Mean percentage pnl per trade
    average_pnl_percent_per_trade = sum(pnl_percent_list) / len(pnl_percent_list)

    # Mean holding period
    average_holding_period_per_trade = sum(holding_days_list) / len(holding_days_list)

    # Winner and Loosers
    winners = 0
    loosers = 0
    amount_of_trades = 0
    for element in pnl_percent_list:
        if element > 0.0:
            winners = winners + 1
        if element <= 0.0:
            loosers = loosers + 1
        amount_of_trades = amount_of_trades + 1

    print(average_pnl_percent_per_trade)
    print(average_holding_period_per_trade)
    print(winners)
    print(loosers)
    print(amount_of_trades)

    # Start trading with fake money
    columns_list = ['total_capital', 'available_capital', 'capital_invested', 'number_of_positions']

    action_dates_list = transaction_history['entry_date'].values.tolist() + transaction_history['exit_date'].values.tolist()
    action_dates_list = sorted(action_dates_list, key=lambda x: datetime.strptime(x, '%Y-%m-%d'))

    start_capital = 100000
    max_open_positions = 20
    df_calculate_trades = pd.DataFrame(index=action_dates_list, columns=columns_list)
