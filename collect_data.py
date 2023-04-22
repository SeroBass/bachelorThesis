import csv
import shutil
import time  # for your API call limits
from datetime import datetime, timedelta
import FundamentalAnalysis as fa
import pandas as pd
import numpy as np
import os
import os.path
import requests
from urllib.request import urlopen
import json
import sys

import graham_strategy


def download_data():
    print('Start downloading data')
    #sys.exit("Exiting the code with sys.exit()!")
    # your Financial Modeling Prep API key
    api_key = "8b7b2301a41406dc331928f7bd7e1cac"

    if os.path.exists('data/financials') == True:
        shutil.rmtree('data/financials')

    os.mkdir('data/financials')

    # define date range and save daily dates
    #dates = [(datetime(2023, 12, 31) - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(365 * 39)]
    #print('download available tickers')
    df_all_tickers = pd.read_json("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=" + api_key)
    ticker_list = []
    dead_tickers_list = []
    used_tickers_list = []

    # get tickers
    # source: https://www.teletrader.com/stoxx-europe-600-eur-price/index/tts-730376 08.04.2023 19:06
    with open('data/tickers/US_short.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for element in text:
        if '/' in element:
            element = element[0:element.index('/')]
        check = df_all_tickers.loc[df_all_tickers[0] == element]
        element_with_dot = element + '.'
        matching_values = df_all_tickers.loc[df_all_tickers[0].str.contains(element_with_dot), 0].tolist()
        if len(check.index) == 1:
            ticker_list.append(element)
        elif len(matching_values) == 1 and len(check.index) != 1:
            ticker_list.append(matching_values[0])
        elif len(matching_values) > 1 and len(check.index) != 1:
            for value in matching_values:
                if element_with_dot in value:
                    ticker_list.append(value)
                break
        elif len(matching_values) == 0 and len(check.index) == 0:
            dead_tickers_list.append(element)
        else:
            print('other cond exists')


    #ticker_list = list(set(ticker_list))

    # create csv sheet for price list
    # with open('daily_prices.csv', 'w', newline='') as csvfile:
    # writer = csv.writer(csvfile, delimiter=',')
    # writer.writerow(['Datum'] + text)
    # for date in dates:
    # writer.writerow([date] + [''] * len(text))

    # start downloading data
    # df_daily_prices = pd.read_csv('daily_prices.csv', index_col='Datum')
    #ticker_list = ['IBM', 'CS']


    i = 0
    for ticker in ticker_list:
        csv_name = str(ticker) + '.csv'
        try:
            url = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/" + ticker + "?limit=120&apikey=8b7b2301a41406dc331928f7bd7e1cac"
            df = pd.read_json(url)
            df = df.drop(['date', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'period', 'link',
                          'finalLink', 'symbol'], axis=1)
            df_balance_sheet = df.set_index(['calendarYear'])
            #len_df_balance_sheet = len(df_balance_sheet.index)

            url = "https://financialmodelingprep.com/api/v3/cash-flow-statement/" + ticker + "?limit=120&apikey=8b7b2301a41406dc331928f7bd7e1cac"
            df = pd.read_json(url)
            df = df.drop(['date', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'period', 'link',
                          'finalLink', 'symbol'], axis=1)
            df_cashflow_statement = df.set_index(['calendarYear'])
            #len_df_cashflow_statement = len(df_cashflow_statement.index)

            url = "https://financialmodelingprep.com/api/v3/income-statement/" + ticker + "?limit=120&apikey=8b7b2301a41406dc331928f7bd7e1cac"
            df = pd.read_json(url)
            df = df.drop(['date', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'period', 'link',
                          'finalLink', 'symbol'], axis=1)
            df_income_statement = df.set_index(['calendarYear'])
            #len_df_income_statement = len(df_income_statement.index)

            url = "https://financialmodelingprep.com/api/v3/ratios/" + ticker + "?limit=40&apikey=8b7b2301a41406dc331928f7bd7e1cac"
            df = pd.read_json(url)
            df['calendarYear'] = pd.DatetimeIndex(df['date']).year
            df = df.drop(['period', 'date', 'symbol'], axis=1)
            df_ratios = df.set_index(['calendarYear'])
            #len_df_ratios = len(df_ratios.index)

            url = "https://financialmodelingprep.com/api/v3/key-metrics/" + ticker + "?limit=40&apikey=8b7b2301a41406dc331928f7bd7e1cac"
            df = pd.read_json(url)
            df['calendarYear'] = pd.DatetimeIndex(df['date']).year
            df = df.drop(['period', 'date', 'symbol'], axis=1)
            df_key_metrics = df.set_index(['calendarYear'])
            #len_df_key_metrics = len(df_key_metrics.index)

            frames = [df_balance_sheet, df_cashflow_statement, df_ratios, df_income_statement, df_key_metrics]
            merged_df = pd.concat(frames, axis=1)
            #len_merged_df = len(merged_df.index)

            start_date = str(merged_df.index[-1]) + "-01-01"

            df_stock_data_detailed = fa.stock_data_detailed(ticker, api_key, begin=start_date, end="2022-12-31")
            end_date = df_stock_data_detailed.index[0]
            dates = [(datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10])) - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(365 * 50)]
            #pd_dates = pd.date_range(start=start_date, end=end_date)

            col_names = merged_df.columns.values.tolist()
            price_list = []
            ticker_list = []
            price_target_list = []
            df_all_data = pd.DataFrame(index=dates, columns=col_names)

            for index, row in df_all_data.iterrows():
                try:
                    price = df_stock_data_detailed.loc[index]['close']
                    price_target = float(price) * 1.5
                except:
                    price = np.nan
                    price_target = np.nan
                price_list.append(price)
                ticker_list.append(ticker)
                price_target_list.append(price_target)

                try:
                    df_all_data.loc[index] = merged_df.loc[int(index[0:4]) - 1]
                except:
                    continue

            df_all_data['price'] = price_list
            df_all_data['ticker'] = ticker_list
            df_all_data['price_target'] = price_target_list

            df_all_data = df_all_data.dropna(subset=['price'])
            #mask = df_all_data.drop('price', axis=1).isna().all(1) & df_all_data['price'].notna()
            #df_all_data = df_all_data[~mask]



            min_count = int(((100-50)/100)*df_all_data.shape[1]+1)
            df_all_data = df_all_data.dropna(axis=0, thresh=min_count)

            if (
                    df_balance_sheet.index[0] == df_cashflow_statement.index[0] and
                    df_cashflow_statement.index[0] == df_income_statement.index[0] and
                    df_income_statement.index[0] == df_ratios.index[0] and
                    df_ratios.index[0] == df_key_metrics.index[0]
            ):
                #print('Start year: ' + (df_all_data.index[-1])[0:4])
                #df_all_data = graham_strategy.search_for_possibilities(ticker, df_all_data)
                df_all_data.to_csv(os.path.join('data/financials/', csv_name), index=True, header=True)
                used_tickers_list.append(ticker)
                print('Successfull: ' + ticker)
            else:
                print('Drop ticker because of year indiscrepancy: ' + ticker)
                dead_tickers_list.append(ticker)
                i = i + 1


            #if i == 1:
            #    df_temp = pd.read_csv(os.path.join('data/financials/', csv_name))
            #    df_temp.to_csv('data/financials/master.csv', index=True, header=True)
            #else:
            #    df_temp = pd.read_csv(os.path.join('data/financials/', csv_name))
            #    df_merge_candidate = pd.read_csv('data/financials/master.csv', index_col=0)
            #    df_master = df_temp.append(df_merge_candidate, ignore_index=True)
            #    os.remove('data/financials/master.csv')
            #    df_master.to_csv('data/financials/master.csv', index=True, header=True)

            #i = i + 1

        except:
            print("Company not found: " + ticker)
            dead_tickers_list.append(ticker)





    with open('data/tickers/stocks_used.txt', 'w') as f:
        for line in used_tickers_list:
            f.write(line)
            f.write('\n')

    with open('data/tickers/stocks_not_used.txt', 'w') as f:
        for line in dead_tickers_list:
            f.write(line)
            f.write('\n')

    print("Finished collecting data.")
