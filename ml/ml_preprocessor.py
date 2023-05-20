import pandas as pd
import os
import os.path
import numpy as np


def set_target():
    print('Setting target for ML strategy')

    # Load transaction histories of Graham 20 and Graham 10 strategies and calculate factors
    transaction_history_graham_20 = pd.read_csv('data/backtesting/transaction_history_graham_20.csv')
    factors_list_20 = []
    for index, row in transaction_history_graham_20.iterrows():
        factors_list_20.append(row['highest_price']/row['entry_price'])

    transaction_history_graham_10 = pd.read_csv('data/backtesting/transaction_history_graham_10.csv')
    factors_list_10 = []
    for index, row in transaction_history_graham_10.iterrows():
        factors_list_10.append(row['highest_price']/row['entry_price'])

    # Calculate mean of both strategy factors and get the better strategy
    try:
        mean_20 = sum(factors_list_20)/len(factors_list_20)
    except:
        mean_20 = 1
    try:
        mean_10 = sum(factors_list_10)/len(factors_list_10)
    except:
        mean_10 = 1

    ml_target = 0
    if mean_20 > mean_10:
        ml_target = mean_20 * 1.01
    else:
        ml_target = mean_10 * 1.01

    # Calculate the target and decide if reached, save file
    with open('logs/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        csv_name = str(ticker) + '.csv'
        df_stock_fund = (pd.read_csv(os.path.join('data/financials/', csv_name), index_col=0)).iloc[::-1]
        iteration_start_at = 0
        goal_reached_list = []

        for index, row in df_stock_fund.iterrows():
            goal_price = row['price'] * ml_target
            df_search_goal = df_stock_fund.drop(df_stock_fund.index[0:iteration_start_at], inplace=False)
            col = df_search_goal['price']
            count = col[col > goal_price].count()
            if count > 0:
                goal_reached_list.append(1)
            else:
                goal_reached_list.append(-1)
            iteration_start_at = iteration_start_at + 1

        df_stock_fund['ml_goal_reached'] = goal_reached_list
        os.remove(os.path.join('data/financials/', csv_name))
        df_stock_fund.to_csv(os.path.join('data/financials/', csv_name), index=True, header=True)


def merge_all_companies():
    print('Merging all dataframes')

    # Merge used companies into one master file
    with open('logs/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    csv_name = str(text[0]) + '.csv'
    df_start = pd.read_csv(os.path.join('data/financials', csv_name))

    i = 1
    while i <= len(text)-2:
        try:
            csv_name = str(text[i]) + '.csv'
            df_merge_candidate = pd.read_csv(os.path.join('data/financials', csv_name))
            df_start = pd.concat([df_merge_candidate, df_start], ignore_index=True)
        except:
            a = 0
        i = i + 1

    df_start.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
    df_start = df_start.drop(['date'], axis=1)
    df_start.to_csv('data/financials/master.csv', index=False, header=True)


def clean_table():
    print('Start cleaning master dataframe')
    df_master = pd.read_csv('data/financials/master.csv', index_col=0)

    # If some kind of zero, replace with nan
    df_master = df_master.replace(0.0, np.nan)
    df_master = df_master.replace(0, np.nan)
    df_master = df_master.replace('0.0', np.nan)
    df_master = df_master.replace('0', np.nan)

    df_master = df_master.replace(np.inf, 10000000000.0)
    df_master = df_master.replace(-np.inf, -10000000000.0)

    percent_nan = 100/df_master.size*df_master.isna().sum().sum()

    count = 0
    for col_name in list(df_master.columns):
        try:
            if 100 / len(df_master.index) * df_master[col_name].isna().sum() > 20:
                df_master = df_master.drop([col_name], axis=1)  # Drop column if more than 20 % nan
                count = count + 1
        except:
            continue

    len_before = len(df_master)
    min_count = int(((100 - 20) / 100) * df_master.shape[1] + 1)
    df_master = df_master.dropna(axis=0, thresh=min_count)  # Drop row if more than 20 % nan

    data = {
        'Initial percent of nan of total data': percent_nan,
        'Removed columns if more than 20% nan': count,
        'Removed rows if more than 20% nan': len_before - len(df_master),
        'Amount of nan replaced with 0.0': df_master.isna().sum().sum(),
        'Amount of rows': len(df_master),
        'Amount of cols': len(list(df_master.columns))
    }

    with open('logs/cleaned_table.txt', 'w') as f:
        for key in data:
            text = str(key) + ': ' + str(data[key])
            f.write(text)
            f.write('\n')

    # Replace all nan's with 0.0 for further calculations
    df_master = df_master.fillna(0.0)
    os.remove('data/financials/master.csv')
    df_master.to_csv('data/financials/master.csv', index=True, header=True)
