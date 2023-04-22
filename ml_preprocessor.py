import pandas as pd
import FundamentalAnalysis as fa
import os
import os.path
import numpy as np

def set_target():
    #api_key = "8b7b2301a41406dc331928f7bd7e1cac"

    #os.mkdir('data/ml_prepared')
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
        #print(goal_reached_list)


        df_stock_fund['ml_goal_reached'] = goal_reached_list
        os.remove(os.path.join('data/financials/', csv_name))
        df_stock_fund.to_csv(os.path.join('data/financials/', csv_name), index=True, header=True)


def ke_ahnig():
    api_key = "8b7b2301a41406dc331928f7bd7e1cac"

    # os.mkdir('data/ml_prepared')

    with open('data/tickers/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        csv_name = str(ticker) + '.csv'
        try:
            df_stock_fund = (pd.read_csv(os.path.join('data/financials/', csv_name), index_col=0)).iloc[::-1]
            start_date = df_stock_fund.index[0]
            # end_date = df_stock_fund.iloc[-1, 0]
            # future_start_date = str(int(start_date[0:4])+1) + str(start_date[4:10])
            df_stock_data_detailed = ((fa.stock_data_detailed(ticker, api_key, begin=start_date))).iloc[
                                     ::-1]

            goal_reached_list = []
            target_price_list = []
            for index, row in df_stock_fund.iterrows():

                goal_price = row['price'] * 1.2
                target_price_list.append(goal_price)
                last_index = str(int((str(index))[0:4]) + 1) + str(index[4:10])
                # last_index = str((int(str(index[0:4])))+1) #+ str(index[4:10])
                df = df_stock_data_detailed.truncate(before=index, after=last_index)
                # print(len(df.index))
                iterator = 0  # len(df.index) - 1
                if len(df.index) > 100:
                    while iterator < len(df.index):
                        if float(df.iloc[iterator, 3]) > goal_price:
                            iterator = len(df.index)
                            goal_reached_list.append(1)

                        if iterator == len(df.index) - 1:
                            goal_reached_list.append(0)
                        iterator = iterator + 1
                else:
                    goal_reached_list.append(np.nan)

            df_stock_fund['ml_goal_reached'] = goal_reached_list
            df_stock_fund['target_price'] = target_price_list
            df_stock_fund = df_stock_fund.dropna(subset=['ml_goal_reached'])
            # os.remove(os.path.join('data/financials/ml_ready', csv_name))
            df_stock_fund.to_csv(os.path.join('data/ml_prepared', csv_name), index=True, header=True)
            print('Success: ' + ticker)
        except:
            print('Could not process company: ' + ticker)

    for ticker in text:
        csv_name = str(ticker) + '.csv'
        if i == 0:
            i = i + 1
            df_temp = pd.read_csv(os.path.join('data/financials', csv_name), index_col=0)
            df_temp.to_csv('data/financials/master.csv', index=True, header=True)
            #os.remove(os.path.join('data/financials/ml_ready', csv_name))
        else:
            df_temp = pd.read_csv(os.path.join('data/financials', csv_name), index_col=0)
            df_merge_candidate = pd.read_csv('data/financials/master.csv', index_col=0)
            df_master = df_temp.append(df_merge_candidate, ignore_index=True)
            os.remove('data/financials/master.csv')
            df_master.to_csv('data/financials/master.csv', index=True, header=True)
            #os.remove(os.path.join('data/financials/ml_ready', csv_name))



def merge_all_companies():

    print('Merging all dataframes')
    with open('data/tickers/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    csv_name = str(text[0]) + '.csv'
    df_start = pd.read_csv(os.path.join('data/financials', csv_name))

    i = 1
    while i <= len(text)-2:
        #try:
        csv_name = str(text[i]) + '.csv'
        df_merge_candidate = pd.read_csv(os.path.join('data/financials', csv_name))
        df_start = pd.concat([df_merge_candidate, df_start], ignore_index=True)
        #df_start = df_start.concat(df_merge_candidate, ignore_index=True)
            #print('Success: ' + text[i])
        #except:
            #print('No company left')
        i = i + 1

    df_start.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
    df_start = df_start[df_start['date'].str.contains('2023|2022') == False]
    df_start = df_start.drop(['date'], axis=1)
    print()
    df_start.to_csv('data/financials/master.csv', index=False, header=True)

    print('Finished merging. Length of index: ', len(df_start.index))

def clean_table():
    print('Start cleaning master dataframe')
    df_master = pd.read_csv('data/financials/master.csv', index_col=0)

    df_master = df_master.replace(0.0, np.nan)
    df_master = df_master.replace(0, np.nan)
    df_master = df_master.replace('0.0', np.nan)
    df_master = df_master.replace('0', np.nan)

    #abc = df_master['cashAndCashEquivalents']

    print('Amount of data: ', df_master.size)
    print('Amount of nan: ', df_master.isna().sum().sum())
    print('% of nan: ', 100/df_master.size*df_master.isna().sum().sum())
    #print(df_master['operatingCycle'].value_counts()[0.0])

    print('Removing columns with more than 20% nan')
    count = 0
    for col_name in list(df_master.columns):
        try:
            if 100 / len(df_master.index) * df_master[col_name].isna().sum() > 20:
                #print('nan in col: ', df_master[col_name].isna().sum(), ' in % ', 100 / len(df_master.index) * df_master[col_name].isna().sum(), ' ', col_name)
                df_master = df_master.drop([col_name], axis=1)
                count = count + 1
        except:
            continue
    print('Removed ', count, ' columns')

    print('Removing rows with more than 20% nan')
    len_before = len(df_master)
    min_count = int(((100 - 20) / 100) * df_master.shape[1] + 1)
    df_master = df_master.dropna(axis=0, thresh=min_count)
    #print('Deleted rows: ', len_before - len(df_master))
    print('Removed ', len_before - len(df_master), ' rows')

    #df_master = df_master.fillna(0.0)

    for col_name in list(df_master.columns):
        try:
            if 100 / len(df_master.index) * df_master[col_name].value_counts()[0.0] >= 50:
                print('Too much 0.0: ', int(100 / len(df_master.index) * df_master[col_name].value_counts()[0.0]), " ", col_name)
                df_master = df_master.drop([col_name], axis=1)
                count = count + 1
        except:
            continue

    print('% of nan: ', 100 / df_master.size * df_master.isna().sum().sum())
    #print('Removed ', count, ' columns')
    print('Replacing nan with 0.0')
    df_master = df_master.fillna(0.0)
    os.remove('data/financials/master.csv')
    df_master.to_csv('data/financials/master.csv', index=True, header=True)