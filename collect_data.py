import shutil
from datetime import datetime, timedelta
import FundamentalAnalysis as fa
import pandas as pd
import numpy as np
import os
import os.path

def download_data():
    print('Start downloading data')

    # your Financial Modeling Prep API key
    api_key = "8b7b2301a41406dc331928f7bd7e1cac"

    # Prepare directory
    if os.path.exists('data/financials') == True:
        shutil.rmtree('data/financials')
    os.mkdir('data/financials')

    # define date range and save daily dates
    df_all_tickers = pd.read_json("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=" + api_key)
    ticker_list = []
    dead_tickers_list = []
    used_tickers_list = []

    # get tickers
    # source: https://www.teletrader.com/stoxx-europe-600-eur-price/index/tts-730376 08.04.2023 19:06
    with open('data/tickers/US_short.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    # Check if ticker is available at financial modeling prep
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

    i = 0
    for ticker in ticker_list:
        csv_name = str(ticker) + '.csv'
        try:
            # Download Balance Sheet
            url = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/" + ticker + "?limit=120&apikey=8b7b2301a41406dc331928f7bd7e1cac"
            df = pd.read_json(url)
            df = df.drop(['date', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'period', 'link', 'finalLink', 'symbol'], axis=1)
            df_balance_sheet = df.set_index(['calendarYear'])

            # Download Cash Flow Statement
            url = "https://financialmodelingprep.com/api/v3/cash-flow-statement/" + ticker + "?limit=120&apikey=8b7b2301a41406dc331928f7bd7e1cac"
            df = pd.read_json(url)
            df = df.drop(['date', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'period', 'link', 'finalLink', 'symbol'], axis=1)
            df_cashflow_statement = df.set_index(['calendarYear'])

            # Download Income Statement
            url = "https://financialmodelingprep.com/api/v3/income-statement/" + ticker + "?limit=120&apikey=8b7b2301a41406dc331928f7bd7e1cac"
            df = pd.read_json(url)
            df = df.drop(['date', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'period', 'link', 'finalLink', 'symbol'], axis=1)
            df_income_statement = df.set_index(['calendarYear'])

            # Download Financial Racios
            url = "https://financialmodelingprep.com/api/v3/ratios/" + ticker + "?limit=40&apikey=8b7b2301a41406dc331928f7bd7e1cac"
            df = pd.read_json(url)
            df['calendarYear'] = pd.DatetimeIndex(df['date']).year
            df = df.drop(['period', 'date', 'symbol'], axis=1)
            df_ratios = df.set_index(['calendarYear'])

            # Download Financial Key Metrics
            url = "https://financialmodelingprep.com/api/v3/key-metrics/" + ticker + "?limit=40&apikey=8b7b2301a41406dc331928f7bd7e1cac"
            df = pd.read_json(url)
            df['calendarYear'] = pd.DatetimeIndex(df['date']).year
            df = df.drop(['period', 'date', 'symbol'], axis=1)
            df_key_metrics = df.set_index(['calendarYear'])

            # Merge downloaded fundamentals into one df
            frames = [df_balance_sheet, df_cashflow_statement, df_ratios, df_income_statement, df_key_metrics]
            merged_df = pd.concat(frames, axis=1)

            # Download price data
            start_date = str(merged_df.index[-1]) + "-01-01"
            df_stock_data_detailed = fa.stock_data_detailed(ticker, api_key, begin=start_date, end="2022-12-31")
            end_date = df_stock_data_detailed.index[0]
            # Define date range
            dates = [(datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10])) - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(365 * 50)]

            # Merge prices, dates, ticker, price target and fundamentals into df_all_data
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

            # Add price, ticker and price target to df
            df_all_data['price'] = price_list
            df_all_data['ticker'] = ticker_list
            df_all_data['price_target'] = price_target_list

            df_all_data = df_all_data.dropna(subset=['price']) # If 'price' is the only data in row, drop row
            min_count = int(((100-50)/100)*df_all_data.shape[1]+1) # If 50% of a row is nan, drop row
            df_all_data = df_all_data.dropna(axis=0, thresh=min_count)

            # Control if concatenation was correct and save df as csv if correct, else drop df
            if (
                    df_balance_sheet.index[0] == df_cashflow_statement.index[0] and
                    df_cashflow_statement.index[0] == df_income_statement.index[0] and
                    df_income_statement.index[0] == df_ratios.index[0] and
                    df_ratios.index[0] == df_key_metrics.index[0]
            ):
                df_all_data.to_csv(os.path.join('data/financials/', csv_name), index=True, header=True)
                used_tickers_list.append(ticker)
                print('Successfull: ' + ticker)
            else:
                print('Drop ticker because of year indiscrepancy: ' + ticker)
                dead_tickers_list.append(ticker)
                i = i + 1
        except:
            print("Company not found: " + ticker)
            dead_tickers_list.append(ticker)

    # Save used tickers into txt file
    with open('data/tickers/stocks_used.txt', 'w') as f:
        for line in used_tickers_list:
            f.write(line)
            f.write('\n')

    # Save droped tickers into txt file
    with open('data/tickers/stocks_not_used.txt', 'w') as f:
        for line in dead_tickers_list:
            f.write(line)
            f.write('\n')

    print("Finished collecting data.")
