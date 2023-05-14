from datetime import date
import pandas as pd
import os
import os.path


def trade_graham_20():
    # Strategy based on Graham Principles
    # Dividend criteria: 20 years
    print('Backtesting Grahams Strategy (20)')
    if os.path.exists('data/backtesting/transaction_history_graham_20.csv') == True:
        os.remove('data/backtesting/transaction_history_graham_20.csv')
    if os.path.exists('data/backtesting') == False:
        os.mkdir('data/backtesting')

    data = {
        'ticker': [],
        'entry_date': [],
        'entry_price': [],
        'last_date': [],
        'holding_days_last_date': [],
        'last_price': [],
        'last_percent': [],
        'highest_price': [],
        'highest_date': [],
        'holding_days_highest_date': [],
        'highest_percent': []
    }
    df_transaction_history = pd.DataFrame(data=data)

    # get tickers
    with open('logs/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        csv_name = str(ticker) + '.csv'
        path = os.path.join('data/financials', csv_name)
        possibilities = (pd.read_csv(path, index_col=0)) #.iloc[::-1]

        entry_price = 0
        position_is_open = 0
        entry_date = ""
        last_day = ""
        last_price = 0
        highest_price = 0
        highest_date = ''

        for index, row in possibilities.iterrows():
            # open position according Grahams Defensive Principles
            if position_is_open == 0 and (
                    row['marketCap'] >= 2000000000 and
                    row['grahams_financial_strength_decision'] == 1 and
                    row['grahams_earnings_stability_decision'] == 1 and
                    row['grahams_20_dividend_stability_decision'] == 1 and
                    row['grahams_earnings_growth_decision'] == 1 and
                    (
                            (row['grahams_pe'] <= 15 and row['grahams_pe'] > 0 and row['grahams_pb'] > 0 and row['grahams_pb'] < 1.33) or
                            (row['grahams_pe'] * row['grahams_pb'] <= 22.5 and row['grahams_pe'] * row['grahams_pb'] > 0)
                    )
            ):
                position_is_open = 1
                entry_date = index
                entry_price = row['price']

            if float(row['price']) > float(highest_price) and position_is_open == 1:
                highest_price = float(row['price'])
                highest_date = index

            last_day = index
            last_price = row['price']

        # if position could not be closed at the end: exit_price = last price
        if position_is_open == 1:
            new_position = pd.Series({
                'ticker': ticker,
                'entry_date': entry_date,
                'entry_price': entry_price,
                'last_date': last_day,
                'holding_days_last_date': date(int(last_day[0:4]), int(last_day[5:7]), int(last_day[8:10])) - date(
                    int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                'last_price': last_price,
                'last_percent': (100/entry_price*last_price)-100,
                'highest_price': highest_price,
                'highest_date': highest_date,
                'holding_days_highest_date': date(int(highest_date[0:4]), int(highest_date[5:7]), int(highest_date[8:10])) - date(
                    int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                'highest_percent': (100/entry_price*highest_price)-100
            })
            df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
    df_transaction_history.to_csv('data/backtesting/transaction_history_graham_20.csv', index=False, header=True)


def trade_graham_10():
    # Strategy based on Graham Principles
    # Dividend criteria: 10 years
    print('Backtesting Grahams Strategy (10)')
    if os.path.exists('data/backtesting/transaction_history_graham_10.csv') == True:
        os.remove('data/backtesting/transaction_history_graham_10.csv')
    if os.path.exists('data/backtesting') == False:
        os.mkdir('data/backtesting')

    data = {
        'ticker': [],
        'entry_date': [],
        'entry_price': [],
        'last_date': [],
        'holding_days_last_date': [],
        'last_price': [],
        'last_percent': [],
        'highest_price': [],
        'highest_date': [],
        'holding_days_highest_date': [],
        'highest_percent': []
    }
    df_transaction_history = pd.DataFrame(data=data)

    # get tickers
    with open('logs/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        csv_name = str(ticker) + '.csv'
        path = os.path.join('data/financials', csv_name)
        possibilities = (pd.read_csv(path, index_col=0)) #.iloc[::-1]

        entry_price = 0
        position_is_open = 0
        entry_date = ""
        last_day = ""
        last_price = 0
        highest_price = 0
        highest_date = ''

        for index, row in possibilities.iterrows():
            # open position according Grahams Defensive Principles
            if position_is_open == 0 and (
                    row['marketCap'] >= 2000000000 and
                    row['grahams_financial_strength_decision'] == 1 and
                    row['grahams_earnings_stability_decision'] == 1 and
                    row['grahams_10_dividend_stability_decision'] == 1 and
                    row['grahams_earnings_growth_decision'] == 1 and
                    (
                            (row['grahams_pe'] <= 15 and row['grahams_pe'] > 0 and row['grahams_pb'] > 0 and row['grahams_pb'] < 1.33) or
                            (row['grahams_pe'] * row['grahams_pb'] <= 22.5 and row['grahams_pe'] * row['grahams_pb'] > 0)
                    )
            ):
                position_is_open = 1
                entry_date = index
                entry_price = row['price']

            if float(row['price']) > float(highest_price) and position_is_open == 1:
                highest_price = float(row['price'])
                highest_date = index

            last_day = index
            last_price = row['price']

        # if position could not be closed at the end: exit_price = last price
        if position_is_open == 1:
            new_position = pd.Series({
                'ticker': ticker,
                'entry_date': entry_date,
                'entry_price': entry_price,
                'last_date': last_day,
                'holding_days_last_date': date(int(last_day[0:4]), int(last_day[5:7]), int(last_day[8:10])) - date(
                    int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                'last_price': last_price,
                'last_percent': (100/entry_price*last_price)-100,
                'highest_price': highest_price,
                'highest_date': highest_date,
                'holding_days_highest_date': date(int(highest_date[0:4]), int(highest_date[5:7]),
                                                  int(highest_date[8:10])) - date(
                    int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                'highest_percent': (100/entry_price*highest_price)-100
            })
            df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
    df_transaction_history.to_csv('data/backtesting/transaction_history_graham_10.csv', index=False, header=True)


def trade_ml():
    # Strategy based on Decision Tree Classifier
    print('Backtesting ML Strategy')
    if os.path.exists('data/backtesting/transaction_history_ml.csv') == True:
        os.remove('data/backtesting/transaction_history_ml.csv')
    if os.path.exists('data/backtesting') == False:
        os.mkdir('data/backtesting')

    data = {
        'ticker': [],
        'entry_date': [],
        'entry_price': [],
        'last_date': [],
        'holding_days_last_date': [],
        'last_price': [],
        'last_percent': [],
        'highest_price': [],
        'highest_date': [],
        'holding_days_highest_date': [],
        'highest_percent': []
    }
    df_transaction_history = pd.DataFrame(data=data)

    # get tickers
    with open('logs/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        csv_name = str(ticker) + '.csv'
        path = os.path.join('data/financials', csv_name)
        possibilities = (pd.read_csv(path, index_col=0)) #.iloc[::-1]

        entry_price = 0
        position_is_open = 0
        entry_date = ""
        last_day = ""
        last_price = 0
        highest_price = 0
        highest_date = ''

        for index, row in possibilities.iterrows():
            # open position according Decision Tree Classifier Principles
            if position_is_open == 0 and \
                    (
                            (
                                    (row['longTermDebt'] <= 924000000.0) and
                                    (row['marketCap'] <= 1804302208.0) and
                                    (row['propertyPlantEquipmentNet'] > 499000.0) and
                                    (row['weightedAverageShsOut'] > 28318029.0) and
                                    (row['tangibleAssetValue'] <= 570517472.0) and
                                    (row['retainedEarnings'] > -1959751.062) and
                                    (row['grahamNumber'] <= 2.941) and
                                    (row['otherCurrentLiabilities'] > 2742000.0) and
                                    (row['grahams_pe'] <= 4261.479)
                            ) or
                            (
                                    (row['longTermDebt'] <= 924000000.0) and
                                    (row['marketCap'] <= 1804302208.0) and
                                    (row['propertyPlantEquipmentNet'] > 499000.0) and
                                    (row['weightedAverageShsOut'] > 28318029.0) and
                                    (row['tangibleAssetValue'] <= 570517472.0) and
                                    (row['retainedEarnings'] > -1959751.062) and
                                    (row['grahamNumber'] > 2.941) and
                                    (row['enterpriseValueMultiple'] <= 20.075) and
                                    (row['grahams_pe'] <= 2214.981) and
                                    (row['grossProfitRatio'] > 0.183) and
                                    (row['retainedEarnings'] <= 329698000.0) and
                                    (row['evToFreeCashFlow'] <= 56.705) and
                                    (row['cashPerShare'] <= 1.442)
                            ) or
                            (
                                    (row['longTermDebt'] <= 924000000.0) and
                                    (row['marketCap'] > 1804302208.0) and
                                    (row['grahams_pe'] <= 572.427) and
                                    (row['weightedAverageShsOutDil'] > 162154512.0) and
                                    (row['fixedAssetTurnover'] > 1.299) and
                                    (row['cashAndCashEquivalents'] <= 257300000.0) and
                                    (row['grahamNumber'] > 2.047) and
                                    (row['enterpriseValue'] <= 4441369856.0) and
                                    (row['dividendPaidAndCapexCoverageRatio'] > -37.081) and
                                    (row['otherNonCashItems'] > -158945976.0) and
                                    (row['grahams_pb'] > -11.642)
                            ) or
                            (
                                    (row['longTermDebt'] <= 924000000.0) and
                                    (row['marketCap'] > 1804302208.0) and
                                    (row['grahams_pe'] <= 572.427) and
                                    (row['weightedAverageShsOutDil'] > 162154512.0) and
                                    (row['fixedAssetTurnover'] > 1.299) and
                                    (row['cashAndCashEquivalents'] > 257300000.0) and
                                    (row['capexToDepreciation'] <= -1.2) and
                                    (row['workingCapital'] > 571000000.0) and
                                    (row['weightedAverageShsOut'] > 159686304.0) and
                                    (row['assetTurnover'] > 0.361) and
                                    (row['grahams_pb'] <= 25.448) and
                                    (row['effectiveTaxRate'] > -0.335) and
                                    (row['eps'] <= 12.74)
                            ) or
                            (
                                    (row['longTermDebt'] <= 924000000.0) and
                                    (row['marketCap'] <= 1804302208.0) and
                                    (row['propertyPlantEquipmentNet'] > 499000.0) and
                                    (row['weightedAverageShsOut'] > 28318029.0) and
                                    (row['tangibleAssetValue'] <= 570517472.0) and
                                    (row['retainedEarnings'] <= -1959751.062) and
                                    (row['totalAssets'] > 45462500.0) and
                                    (row['commonStock'] > 866000.0) and
                                    (row['operatingCashFlowSalesRatio'] <= 0.179) and
                                    (row['capexToDepreciation'] <= -0.113) and
                                    (row['tangibleBookValuePerShare'] <= 0.966) and
                                    (row['operatingCashFlowPerShare.1'] <= 2.801)
                            ) or
                            (
                                    (row['longTermDebt'] <= 924000000.0) and
                                    (row['marketCap'] <= 1804302208.0) and
                                    (row['propertyPlantEquipmentNet'] > 499000.0) and
                                    (row['weightedAverageShsOut'] <= 28318029.0) and
                                    (row['marketCap'] <= 14577595.0) and
                                    (row['capexToDepreciation'] > -139.175) and
                                    (row['grahams_pb'] <= 1.909) and
                                    (row['otherInvestingActivites'] > -455000.0) and
                                    (row['weightedAverageShsOut'] > 2336798.0)
                            ) or
                            (
                                    (row['longTermDebt'] > 924000000.0) and
                                    (row['interestExpense'] <= 8500000.0) and
                                    (row['cashPerShare'] <= 13.27) and
                                    (row['retainedEarnings'] > -123587500.0) and
                                    (row['cashAtEndOfPeriod'] <= 139317280.0) and
                                    (row['priceToSalesRatio'] <= 4.236) and
                                    (row['weightedAverageShsOut'] > 44580710.0) and
                                    (row['returnOnTangibleAssets'] <= 0.064)
                            ) or
                            (
                                    (row['longTermDebt'] <= 924000000.0) and
                                    (row['marketCap'] <= 1804302208.0) and
                                    (row['propertyPlantEquipmentNet'] > 499000.0) and
                                    (row['weightedAverageShsOut'] <= 28318029.0) and
                                    (row['marketCap'] > 14577595.0) and
                                    (row['depreciationAndAmortization'] <= 24452000.0) and
                                    (row['shareholdersEquityPerShare'] > 3.679) and
                                    (row['evToSales'] > 0.596) and
                                    (row['totalNonCurrentAssets'] <= 377800304.0) and
                                    (row['retainedEarnings'] > -1383466.0) and
                                    (row['ebitdaratio'] <= 0.534) and
                                    (row['quickRatio'] <= 1.48) and
                                    (row['grahams_pb'] <= 14.411) and
                                    (row['quickRatio'] > 0.085) and
                                    (row['tangibleAssetValue'] > 13669000.0) and
                                    (row['grahams_pe'] > -1639.183) and
                                    (row['incomeTaxExpense'] <= 11668500.0) and
                                    (row['peRatio'] > -118.6)
                            ) or
                            (
                                    (row['longTermDebt'] <= 924000000.0) and
                                    (row['marketCap'] <= 1804302208.0) and
                                    (row['propertyPlantEquipmentNet'] > 499000.0) and
                                    (row['weightedAverageShsOut'] > 28318029.0) and
                                    (row['tangibleAssetValue'] > 570517472.0) and
                                    (row['interestExpense'] <= 14533.5) and
                                    (row['otherCurrentLiabilities'] > 36283134.0) and
                                    (row['grahams_pb'] <= 14.995) and
                                    (row['longTermDebt'] > 2374026.0)
                            ) or
                            (
                                    (row['longTermDebt'] <= 924000000.0) and
                                    (row['marketCap'] <= 1804302208.0) and
                                    (row['propertyPlantEquipmentNet'] > 499000.0) and
                                    (row['weightedAverageShsOut'] > 28318029.0) and
                                    (row['tangibleAssetValue'] <= 570517472.0) and
                                    (row['retainedEarnings'] > -1959751.062) and
                                    (row['grahamNumber'] > 2.941) and
                                    (row['enterpriseValueMultiple'] <= 20.075) and
                                    (row['grahams_pe'] <= 2214.981) and
                                    (row['grossProfitRatio'] > 0.183) and
                                    (row['retainedEarnings'] <= 329698000.0) and
                                    (row['evToFreeCashFlow'] <= 56.705) and
                                    (row['cashPerShare'] > 1.442) and
                                    (row['capexToRevenue'] <= -0.013) and
                                    (row['commonStock'] > 1029850.344)
                            )
                    ):
                position_is_open = 1
                entry_date = index
                entry_price = row['price']

            if float(row['price']) > float(highest_price) and position_is_open == 1:
                highest_price = float(row['price'])
                highest_date = index

            last_day = index
            last_price = row['price']

        # if position could not be closed at the end: exit_price = last price
        if position_is_open == 1:
            new_position = pd.Series({
                'ticker': ticker,
                'entry_date': entry_date,
                'entry_price': entry_price,
                'last_date': last_day,
                'holding_days_last_date': date(int(last_day[0:4]), int(last_day[5:7]), int(last_day[8:10])) - date(
                    int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                'last_price': last_price,
                'last_percent': (100/entry_price*last_price)-100,
                'highest_price': highest_price,
                'highest_date': highest_date,
                'holding_days_highest_date': date(int(highest_date[0:4]), int(highest_date[5:7]),
                                                  int(highest_date[8:10])) - date(
                    int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])),
                'highest_percent': (100/entry_price*highest_price)-100
            })
            df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
    df_transaction_history.to_csv('data/backtesting/transaction_history_ml.csv', index=False, header=True)
