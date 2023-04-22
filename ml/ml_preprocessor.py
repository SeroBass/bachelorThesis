import pandas as pd
import os
import os.path
import numpy as np

def set_target():
    print('Setting target for ML strategy')

    with open('data/tickers/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        csv_name = str(ticker) + '.csv'

        df_stock_fund = (pd.read_csv(os.path.join('data/financials/', csv_name), index_col=0)).iloc[::-1]
        iteration_start_at = 0
        goal_reached_list = []

        for index, row in df_stock_fund.iterrows():
            goal_price = row['price_target']
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
    with open('data/tickers/stocks_used.txt', 'r') as f:
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
            print('No company left')
        i = i + 1

    df_start.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
    #df_start = df_start[df_start['date'].str.contains('2023|2022') == False]
    df_start = df_start.drop(['date'], axis=1)
    df_start.to_csv('data/financials/master.csv', index=False, header=True)
    print('Finished merging. Length of index: ', len(df_start.index))

def clean_table():
    print('Start cleaning master dataframe')
    df_master = pd.read_csv('data/financials/master.csv', index_col=0)

    df_master = df_master.replace(0.0, np.nan)
    df_master = df_master.replace(0, np.nan)
    df_master = df_master.replace('0.0', np.nan)
    df_master = df_master.replace('0', np.nan)

    df_master = df_master.replace(np.inf, 10000000000.0)
    df_master = df_master.replace(-np.inf, -10000000000.0)

    print('Amount of data: ', df_master.size)
    print('Amount of nan: ', df_master.isna().sum().sum())
    print('% of nan: ', 100/df_master.size*df_master.isna().sum().sum())

    print('Removing columns and rows with more than 20% nan')
    count = 0
    for col_name in list(df_master.columns):
        try:
            if 100 / len(df_master.index) * df_master[col_name].isna().sum() > 20:
                df_master = df_master.drop([col_name], axis=1)
                count = count + 1
        except:
            continue

    len_before = len(df_master)
    min_count = int(((100 - 20) / 100) * df_master.shape[1] + 1)
    df_master = df_master.dropna(axis=0, thresh=min_count)

    print('Removed ', len_before - len(df_master), ' rows')
    print('Removed ', count, ' columns')

    print('% of nan: ', 100 / df_master.size * df_master.isna().sum().sum())
    print('Replacing nan with 0.0')
    df_master = df_master.fillna(0.0)
    os.remove('data/financials/master.csv')
    df_master.to_csv('data/financials/master.csv', index=True, header=True)
