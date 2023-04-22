import csv
import shutil
import sys
import time  # for your API call limits
from datetime import datetime, timedelta, date
import FundamentalAnalysis as fa
import pandas as pd
import os
import os.path
import requests
from urllib.request import urlopen
import json

def trade_graham_50():
    print('Backtesting Grahams Strategy')
    if os.path.exists('data/backtesting/transaction_history_graham_50.csv') == True:
        os.remove('data/backtesting/transaction_history_graham_50.csv')

    amount_per_position = 1000
    commission_costs = 20

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
        exit_date = ""
        exit_price = ""
        pnl = ""
        last_day = ""
        last_price = 0

        for index, row in possibilities.iterrows():
            # open position
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

            # close position
            if row['price'] > price_target and position_is_open == 1:
                exit_date = index
                exit_price = row['price']
                pnl = (100/entry_price*exit_price)-100
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
                df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T],
                                                   ignore_index=True)
                entry_price = 0
                price_target = 0
                position_is_open = 0
                entry_date = ""
                exit_date = ""
                exit_price = ""
                pnl = ""
            last_day = index
            last_price = row['price']

        # if position could not be closed at the end
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
            df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T],
                                               ignore_index=True)
    df_transaction_history.to_csv('data/backtesting/transaction_history_graham_50.csv')
    print('Finished Backtesting')

def trade_ml1():
    print('Backtesting ML Strategy')
    if os.path.exists('data/backtesting/transaction_history_ml1.csv') == True:
        os.remove('data/backtesting/transaction_history_ml1.csv')

    amount_per_position = 1000
    commission_costs = 20

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
        print('Backtesting ', ticker)

        entry_price = 0
        price_target = 0
        position_is_open = 0
        entry_date = ""
        exit_date = ""
        exit_price = ""
        pnl = ""
        last_day = ""
        last_price = 0

        for index, row in possibilities.iterrows():
            # open position
            if (row['operatingCycle'] > 20.591) and (row['operatingCashFlowPerShare.1'] <= 9.243) and (row['enterpriseValue'] <= 62463451136.0) and (row['capexToRevenue'] > -0.127) and (row['interestCoverage.1'] <= 9.425) and (row['longTermDebt'] <= 8391500032.0) and (row['ebtPerEbit'] <= 4.555) and (row['grahamNumber'] > 0.551) and (row['pocfratio'] > -46.315) and (row['grahams_pe'] <= 65.331) and (row['revenuePerShare'] > 0.674) and position_is_open == 0:
                position_is_open = 1
                entry_date = index
                entry_price = row['price']
                price_target = row['price_target']

            # close position
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
                    'holding_days': date(int(exit_date[0:4]), int(exit_date[5:7]), int(exit_date[8:10])) - date(
                        int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                    'pnl (%)': pnl
                })
                df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T],
                                                   ignore_index=True)
                entry_price = 0
                price_target = 0
                position_is_open = 0
                entry_date = ""
                exit_date = ""
                exit_price = ""
                pnl = ""
            last_day = index
            last_price = row['price']

        # if position could not be closed at the end
        if position_is_open == 1:
            new_position = pd.Series({
                'ticker': ticker,
                'position_is_open': 1,
                'entry_date': entry_date,
                'entry_price': entry_price,
                'goal_price': price_target,
                'exit_date': last_day,
                'exit_price': last_price,
                'holding_days': date(int(last_day[0:4]), int(last_day[5:7]), int(last_day[8:10])) - date(
                    int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                'pnl (%)': (100 / entry_price * last_price) - 100
            })
            df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T],
                                               ignore_index=True)
    df_transaction_history.to_csv('data/backtesting/transaction_history_ml1.csv')
    print('Finished Backtesting ML')

def trade_graham_1():
    if os.path.exists('data/backtesting/transaction_history_graham_1.csv') == True:
        os.remove('data/backtesting/transaction_history_graham_1.csv')

    amount_per_position = 1000
    commission_costs = 20

    data = {
        'ticker': [],
        'position_is_open': [],
        'entry_date': [],
        'entry_price': [],
        'amount_of_shares': [],
        'exit_date': [],
        'exit_price': [],
        'pnl': []
    }
    df_transaction_history = pd.DataFrame(data=data)

    # get tickers
    with open('data/tickers/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        csv_name = str(ticker) + '.csv'
        try:
            path = os.path.join('data/financials', csv_name)
            possibilities = pd.read_csv(path)
            number_of_rows = len(possibilities.index)

            while number_of_rows >= 1:
                number_of_rows = number_of_rows - 1
                open_positions = df_transaction_history.loc[df_transaction_history['position_is_open'] == 1]
                if possibilities.loc[number_of_rows]['grahams_is_buy_decision'] == 1 and ticker not in set(open_positions['ticker']):
                    new_position = pd.Series({
                        'ticker': ticker,
                        'position_is_open': possibilities.loc[number_of_rows]['grahams_is_buy_decision'],
                        'entry_date': possibilities.loc[number_of_rows][0],
                        'entry_price': possibilities.loc[number_of_rows]['price'],
                        'amount_of_shares': int(amount_per_position/possibilities.loc[number_of_rows]['price']),
                        'exit_date': -1,
                        'exit_price': -1,
                        'pnl': 0
                    })
                    df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
                    print('New position: ' + ticker)

                if possibilities.loc[number_of_rows]['grahams_is_buy_decision'] == 0 and ticker in set(open_positions['ticker']):
                    mask = (df_transaction_history['ticker'] == ticker) & (df_transaction_history['position_is_open'] == 1)
                    filtered_df = df_transaction_history.loc[mask]
                    index = filtered_df.index[0]

                    df_transaction_history.at[index, 'position_is_open'] = possibilities.loc[number_of_rows]['grahams_is_buy_decision']
                    df_transaction_history.at[index, 'exit_date'] = possibilities.loc[number_of_rows][0]
                    df_transaction_history.at[index, 'exit_price'] = possibilities.loc[number_of_rows]['price']
                    df_transaction_history.at[index, 'pnl'] = (df_transaction_history.at[index, 'exit_price'] - df_transaction_history.at[index, 'entry_price']) * df_transaction_history.at[index, 'amount_of_shares'] - commission_costs
            print("Finished Backtesting of: " + ticker)
        except:
            print("Not found: " + ticker)
    df_transaction_history.to_csv('data/backtesting/transaction_history_graham_1.csv')

def trade_graham_2():
    if os.path.exists('data/backtesting/transaction_history_graham_2.csv') == True:
        os.remove('data/backtesting/transaction_history_graham_2.csv')

    amount_per_position = 1000
    commission_costs = 20

    data = {
        'ticker': [],
        'position_is_open': [],
        'entry_date': [],
        'entry_price': [],
        'amount_of_shares': [],
        'exit_date': [],
        'exit_price': [],
        'pnl': []
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

        if 1 in possibilities['grahams_is_buy_decision'].unique():
            for index, row in possibilities.iterrows():
                open_positions = df_transaction_history.loc[df_transaction_history['position_is_open'] == 1]
                if row['grahams_is_buy_decision'] == 1 and ticker not in set(open_positions['ticker']):
                    new_position = pd.Series({
                        'ticker': ticker,
                        'position_is_open': 1,
                        'entry_date': index,
                        'entry_price': row['price'],
                        'amount_of_shares': int(amount_per_position / row['price']),
                        'exit_date': possibilities.index[-1],
                        'exit_price': (possibilities.iloc[-1])['price'],
                        'pnl': ((possibilities.iloc[-1])['price'] - row['price']) * int(amount_per_position / row['price']) - commission_costs
                    })
                    df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
                    #print('New position: ' + ticker)
        print("Finished Backtesting of: " + ticker)
    df_transaction_history.to_csv('data/backtesting/transaction_history_graham_2.csv')

def trade_graham_3():
    if os.path.exists('data/backtesting/transaction_history_graham_3.csv') == True:
        os.remove('data/backtesting/transaction_history_graham_3.csv')

    amount_per_position = 1000
    commission_costs = 20

    data = {
        'ticker': [],
        'position_is_open': [],
        'entry_date': [],
        'entry_price': [],
        'amount_of_shares': [],
        'exit_date': [],
        'exit_price': [],
        'pnl': []
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
        #number_of_rows = len(possibilities.index)


        for index, row in possibilities.iterrows():
            open_positions = df_transaction_history.loc[df_transaction_history['position_is_open'] == 1]
            if row['grahams_company_size_decision'] == 1 and row['grahams_earnings_stability_decision'] == 1 and row['grahams_earnings_growth_decision'] == 1 and row['grahams_pe_pb_decision'] == 1 and ticker not in set(open_positions['ticker']):
                new_position = pd.Series({
                    'ticker': ticker,
                    'position_is_open': 1,
                    'entry_date': index,
                    'entry_price': row['price'],
                    'amount_of_shares': int(amount_per_position / row['price']),
                    'exit_date': possibilities.index[-1],
                    'exit_price': (possibilities.iloc[-1])['price'],
                    'pnl': ((possibilities.iloc[-1])['price'] - row['price']) * int(amount_per_position / row['price']) - commission_costs
                })
                df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
                print('New position: ' + ticker)

        print("Finished Backtesting of: " + ticker)

        #print("Not found: " + ticker)
    df_transaction_history.to_csv('data/backtesting/transaction_history_graham_3.csv')