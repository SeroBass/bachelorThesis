from datetime import date
import pandas as pd
import os
import os.path

def trade_graham_50():
    # Strategy based on Graham Principles
    # Target = Entry-Price * 1.5 (therefore 50% gain)
    print('Backtesting Grahams Strategy')
    if os.path.exists('data/backtesting/transaction_history_graham_50.csv') == True:
        os.remove('data/backtesting/transaction_history_graham_50.csv')

    data = {
        'ticker': [],
        'position_is_open': [],
        'entry_date': [],
        'entry_price': [],
        'goal_price': [],
        'exit_date': [],
        'exit_price': [],
        'holding_days': [],
        'pnl (%)': []
    }
    df_transaction_history = pd.DataFrame(data=data)

    # get tickers
    with open('data/tickers/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        csv_name = str(ticker) + '.csv'
        path = os.path.join('data/financials', csv_name)
        possibilities = (pd.read_csv(path, index_col=0)).iloc[::-1]

        entry_price = 0
        price_target = 0
        position_is_open = 0
        entry_date = ""
        last_day = ""
        last_price = 0

        for index, row in possibilities.iterrows():
            # open position according Grahams Defensive Principles
            if (
                    row['marketCap'] >= 2000000000 and
                    row['grahams_financial_strength_decision'] == 1 and
                    row['grahams_earnings_stability_decision'] == 1 and
                    row['grahams_dividend_stability_decision'] == 1 and
                    row['grahams_earnings_growth_decision'] == 1 and
                    row['grahams_pe'] <= 15 and
                    row['grahams_pe'] > 0 and
                    row['grahams_pb'] > 0 and
                    row['grahams_pb'] < 1.33 and
                    position_is_open == 0
            ):
                position_is_open = 1
                entry_date = index
                entry_price = row['price']
                price_target = row['price_target']

            # close position when gain > +50%
            if row['price'] > price_target and position_is_open == 1:
                exit_date = index
                exit_price = row['price']
                pnl = (100 / entry_price*exit_price) - 100
                position_is_open = 0

                new_position = pd.Series({
                    'ticker': ticker,
                    'position_is_open': position_is_open,
                    'entry_date': entry_date,
                    'entry_price': entry_price,
                    'goal_price': price_target,
                    'exit_date': exit_date,
                    'exit_price': exit_price,
                    'holding_days': date(int(exit_date[0:4]), int(exit_date[5:7]), int(exit_date[8:10])) - date(int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                    'pnl (%)': pnl
                })
                df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
                entry_price = 0
                price_target = 0
                position_is_open = 0
                entry_date = ""
            last_day = index
            last_price = row['price']

        # if position could not be closed at the end: exit_price = last price
        if position_is_open == 1:
            new_position = pd.Series({
                'ticker': ticker,
                'position_is_open': 1,
                'entry_date': entry_date,
                'entry_price': entry_price,
                'goal_price': price_target,
                'exit_date': last_day,
                'exit_price': last_price,
                'holding_days': date(int(last_day[0:4]), int(last_day[5:7]), int(last_day[8:10])) - date(int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                'pnl (%)': (100/entry_price*last_price)-100
            })
            df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
    df_transaction_history.to_csv('data/backtesting/transaction_history_graham_50.csv')
    print('Finished Backtesting')

def trade_ml_50():
    # Strategy based on Decision Tree Classifier
    # Target = Entry-Price * 1.5 (therefore 50% gain)
    print('Backtesting ML Strategy')
    if os.path.exists('data/backtesting/transaction_history_ml_50.csv') == True:
        os.remove('data/backtesting/transaction_history_ml_50.csv')

    data = {
        'ticker': [],
        'position_is_open': [],
        'entry_date': [],
        'entry_price': [],
        'goal_price': [],
        'exit_date': [],
        'exit_price': [],
        'holding_days': [],
        'pnl (%)': []
    }
    df_transaction_history = pd.DataFrame(data=data)

    # get tickers
    with open('data/tickers/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        csv_name = str(ticker) + '.csv'
        path = os.path.join('data/financials', csv_name)
        possibilities = pd.read_csv(path, index_col=0)

        entry_price = 0
        price_target = 0
        position_is_open = 0
        entry_date = ""
        last_day = ""
        last_price = 0

        for index, row in possibilities.iterrows():
            # open position according Decision Tree Classifier Principles
            if position_is_open == 0 and (
                    () or
                    () or
                    () or
                    () or
                    () or
                    () or
                    () or
                    ()
            ):
                print('Hello')
                position_is_open = 1
                entry_date = index
                entry_price = row['price']
                price_target = row['price_target']

            # close position when gain > +50%
            if row['price'] > price_target and position_is_open == 1:
                exit_date = index
                exit_price = row['price']
                pnl = (100 / entry_price * exit_price) - 100
                position_is_open = 0

                new_position = pd.Series({
                    'ticker': ticker,
                    'position_is_open': position_is_open,
                    'entry_date': entry_date,
                    'entry_price': entry_price,
                    'goal_price': price_target,
                    'exit_date': exit_date,
                    'exit_price': exit_price,
                    'holding_days': date(int(exit_date[0:4]), int(exit_date[5:7]), int(exit_date[8:10])) - date(int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                    'pnl (%)': pnl
                })
                df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
                entry_price = 0
                price_target = 0
                position_is_open = 0
                entry_date = ""
            last_day = index
            last_price = row['price']

        # if position could not be closed at the end: exit_price = last price
        if position_is_open == 1:
            new_position = pd.Series({
                'ticker': ticker,
                'position_is_open': 1,
                'entry_date': entry_date,
                'entry_price': entry_price,
                'goal_price': price_target,
                'exit_date': last_day,
                'exit_price': last_price,
                'holding_days': date(int(last_day[0:4]), int(last_day[5:7]), int(last_day[8:10])) - date(int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])), 'pnl (%)': (100 / entry_price * last_price) - 100
            })
            df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
    df_transaction_history.to_csv('data/backtesting/transaction_history_ml_50.csv')
    print('Finished Backtesting ML')
