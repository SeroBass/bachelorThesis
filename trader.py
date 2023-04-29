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
    if os.path.exists('data/backtesting') == False:
        os.mkdir('data/backtesting')

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
    if os.path.exists('data/backtesting') == False:
        os.mkdir('data/backtesting')

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
            if position_is_open == 0 and \
                    (
                            (
                                (row['longTermDebt'] <= 1376553984.0) and
                                (row['capexToRevenue'] <= -0.003) and
                                (row['weightedAverageShsOut'] > 36000304.0) and
                                (row['quickRatio'] <= 4.476) and
                                (row['fixedAssetTurnover'] <= 240.432) and
                                (row['marketCap'] <= 1734333312.0) and
                                (row['grossProfitMargin'] > 0.149) and
                                (row['pretaxProfitMargin'] <= 1.738) and
                                (row['enterpriseValueOverEBITDA'] > -34.013) and
                                (row['priceEarningsRatio'] > -562.512) and
                                (row['cashAndShortTermInvestments'] > 44500.0) and
                                (row['freeCashFlowYield'] <= 0.509) and
                                (row['debtToAssets'] > 0.195) and
                                (row['peRatio'] <= 519.109) and
                                (row['capitalExpenditureCoverageRatio'] > -35.982) and
                                (row['changeInWorkingCapital'] > -151882000.0) and
                                (row['ebtPerEbit'] <= 2.807) and
                                (row['othertotalStockholdersEquity'] > -182028504.0) and
                                (row['pocfratio'] > -35.836) and
                                (row['grahams_pe'] > -62.328) and
                                (row['netDebt'] > -62692500.0) and
                                (row['returnOnTangibleAssets'] <= 0.288) and
                                (row['revenue'] > 19406500.0) and
                                (row['dividendPaidAndCapexCoverageRatio'] > -140.411) and
                                (row['shareholdersEquityPerShare'] <= 33.803)
                            ) or
                            (
                                (row['longTermDebt'] <= 1376553984.0) and
                                (row['marketCap'] > 2403451136.0) and
                                (row['effectiveTaxRate'] > 0.278) and
                                (row['grossProfit'] > 877150016.0) and
                                (row['retainedEarnings'] > -1172814976.0) and
                                (row['grahamNetNet'] <= 59.825) and
                                (row['effectiveTaxRate'] <= 5.543) and
                                (row['totalLiabilitiesAndTotalEquity'] > 1865979520.0) and
                                (row['roic'] <= 2.151) and
                                (row['evToOperatingCashFlow'] <= 91.623) and
                                (row['bookValuePerShare'] > -0.288) and
                                (row['capexToRevenue'] <= -0.007) and
                                (row['pretaxProfitMargin'] <= 0.387) and
                                (row['incomeQuality'] <= 3.768) and
                                (row['currentRatio.1'] > 0.75) and
                                (row['grahamNumber'] > 1.958) and
                                (row['priceFairValue'] <= 21.872) and
                                (row['freeCashFlowYield'] <= 0.148) and
                                (row['grahams_pb'] <= 223.473) and
                                (row['priceEarningsToGrowthRatio'] <= 14.001) and
                                (row['cashFlowToDebtRatio'] > 0.219) and
                                (row['capexPerShare'] > -3.786) and
                                (row['totalNonCurrentAssets'] <= 82947502080.0) and
                                (row['returnOnTangibleAssets'] <= 0.239) and
                                (row['returnOnEquity'] <= 0.6)
                            ) or
                            (
                                (row['longTermDebt'] > 1376553984.0) and
                                (row['interestExpense'] <= 9500000.0) and
                                (row['cashPerShare'] <= 17.063) and
                                (row['totalNonCurrentAssets'] <= 81734000640.0) and
                                (row['priceToSalesRatio'] <= 1.467) and
                                (row['priceEarningsToGrowthRatio'] <= 17.027) and
                                (row['otherNonCurrentLiabilities'] > -1076500032.0) and
                                (row['revenuePerShare'] <= 275.245) and
                                (row['returnOnCapitalEmployed'] <= 0.484) and
                                (row['longTermDebt'] <= 19844656128.0) and
                                (row['netCashProvidedByOperatingActivities'] > -271500000.0) and
                                (row['returnOnTangibleAssets'] <= 0.172) and
                                (row['fixedAssetTurnover'] <= 30.926) and
                                (row['changeInWorkingCapital'] > -3578077056.0) and
                                (row['cashPerShare.1'] <= 15.388) and
                                (row['enterpriseValueOverEBITDA'] > -151.248) and
                                (row['dividendPaidAndCapexCoverageRatio'] <= 40.668) and
                                (row['returnOnAssets'] <= 0.089)
                            ) or
                            (
                                (row['longTermDebt'] <= 1376553984.0) and
                                (row['capexToRevenue'] <= -0.003) and
                                (row['marketCap'] <= 2403451136.0) and
                                (row['depreciationAndAmortization.1'] > -249611.5) and
                                (row['weightedAverageShsOut'] <= 5300201.5) and
                                (row['priceCashFlowRatio'] <= 106.291) and
                                (row['commonStock'] <= 22504908.0) and
                                (row['returnOnCapitalEmployed'] > -2.646) and
                                (row['effectiveTaxRate'] > -9.003) and
                                (row['capexToDepreciation'] > -204.681) and
                                (row['investmentsInPropertyPlantAndEquipment'] <= -1467.0) and
                                (row['fixedAssetTurnover'] <= 29.597) and
                                (row['priceFairValue'] <= 17.879) and
                                (row['operatingCashFlowPerShare'] > -226.201) and
                                (row['otherNonCashItems'] <= 30282304.0) and
                                (row['grahams_pb'] <= 11.314) and
                                (row['grahamNetNet'] <= 1.159) and
                                (row['totalLiabilitiesAndTotalEquity'] > 2242728.0) and
                                (row['grahamNumber'] > 0.448) and
                                (row['otherFinancingActivites'] <= 756512016.0) and
                                (row['cashAtBeginningOfPeriod'] > -8205000.0) and
                                (row['retainedEarnings'] > -49737000.0)
                            ) or
                            (
                                (row['longTermDebt'] <= 1376553984.0) and
                                (row['capexToRevenue'] <= -0.003) and
                                (row['marketCap'] <= 2403451136.0) and
                                (row['weightedAverageShsOut'] > 36000304.0) and
                                (row['revenue'] > 17000244.0) and
                                (row['quickRatio'] <= 4.476) and
                                (row['fixedAssetTurnover'] <= 240.432) and
                                (row['marketCap'] > 1734333312.0) and
                                (row['returnOnCapitalEmployed'] > 0.038) and
                                (row['debtEquityRatio'] <= 1.759) and
                                (row['netCashUsedProvidedByFinancingActivities'] > -431500000.0) and
                                (row['averagePayables'] <= 956600000.0) and
                                (row['quickRatio'] <= 2.203) and
                                (row['grahams_pb'] > -808.09) and
                                (row['otherCurrentLiabilities'] > 33699000.0) and
                                (row['otherNonCashItems'] > -196921784.0) and
                                (row['incomeTaxExpense'] > -18029000.0) and
                                (row['operatingCashFlowPerShare.1'] <= 6.89) and
                                (row['grahams_pe'] > -1.3435138738225152e+18) and
                                (row['currentRatio.1'] <= 3.962) and
                                (row['investmentsInPropertyPlantAndEquipment'] > -621600000.0) and
                                (row['grossProfitMargin'] > 0.159) and
                                (row['longTermDebt'] <= 1325712448.0) and
                                (row['totalStockholdersEquity'] <= 1934747008.0) and
                                (row['otherCurrentLiabilities'] > 38137500.0) and
                                (row['otherFinancingActivites'] <= 841740000.0) and
                                (row['capitalExpenditure'] > -540902928.0)
                            ) or
                            (
                                (row['longTermDebt'] > 1376553984.0) and
                                (row['interestExpense'] > 9500000.0) and
                                (row['priceToSalesRatio'] <= 0.701) and
                                (row['enterpriseValue'] <= 39012579328.0) and
                                (row['propertyPlantEquipmentNet'] > 1084880000.0) and
                                (row['weightedAverageShsOutDil'] <= 814486272.0) and
                                (row['weightedAverageShsOut'] > 178793224.0) and
                                (row['cashAtEndOfPeriod'] <= 5135500032.0) and
                                (row['othertotalStockholdersEquity'] <= 14350219264.0) and
                                (row['roic'] <= 0.254) and
                                (row['interestExpense'] <= 736500000.0) and
                                (row['grahams_pb'] <= 273.582) and
                                (row['ebtPerEbit'] <= 2.264) and
                                (row['grossProfit'] <= 9106999808.0) and
                                (row['debtToAssets'] > 0.413) and
                                (row['priceToSalesRatio.1'] <= 0.664) and
                                (row['grahams_pb'] <= 247.973)
                            ) or
                            (
                                (row['longTermDebt'] <= 1376553984.0) and
                                (row['capexToRevenue'] <= -0.003) and
                                (row['marketCap'] > 2403451136.0) and
                                (row['effectiveTaxRate'] <= 0.278) and
                                (row['longTermDebtToCapitalization'] <= 0.082) and
                                (row['otherNonCurrentLiabilities'] > -398164496.0) and
                                (row['freeCashFlowOperatingCashFlowRatio'] <= 0.886) and
                                (row['grahams_pe'] <= 2123.503) and
                                (row['returnOnCapitalEmployed'] > 0.164) and
                                (row['totalDebt'] <= 3987164160.0) and
                                (row['operatingExpenses'] > 34811000.0) and
                                (row['dividendPaidAndCapexCoverageRatio'] > -56.132) and
                                (row['tangibleAssetValue'] > -646789472.0) and
                                (row['weightedAverageShsOut'] <= 3967938176.0) and
                                (row['priceCashFlowRatio'] <= 38.197) and
                                (row['grahams_pe'] <= 2034.099) and
                                (row['totalStockholdersEquity'] > 523154480.0) and
                                (row['incomeBeforeTaxRatio'] <= 0.944) and
                                (row['enterpriseValueOverEBITDA'] <= 19.174) and
                                (row['capitalExpenditure'] <= -37815000.0) and
                                (row['longTermDebt'] <= 1065033760.0) and
                                (row['accountPayables'] > 11367000.0)
                            ) or
                            (
                                (row['longTermDebt'] <= 1376553984.0) and
                                (row['capexToRevenue'] <= -0.003) and
                                (row['marketCap'] <= 2403451136.0) and
                                (row['weightedAverageShsOut'] <= 36000304.0) and
                                (row['depreciationAndAmortization.1'] > -249611.5) and
                                (row['weightedAverageShsOut'] > 5300201.5) and
                                (row['operatingIncomeRatio'] > 0.058) and
                                (row['earningsYield'] > 0.056) and
                                (row['interestExpense'] > -368000.0) and
                                (row['capexToRevenue'] > -0.771) and
                                (row['cashAtBeginningOfPeriod'] > 233296.0) and
                                (row['totalEquity'] <= 3299604992.0) and
                                (row['incomeTaxExpense'] <= 22100000.0) and
                                (row['tangibleAssetValue'] > -233794008.0) and
                                (row['incomeBeforeTaxRatio'] > 0.039) and
                                (row['interestDebtPerShare'] > 0.0) and
                                (row['freeCashFlowPerShare'] > -10.516) and
                                (row['capexToRevenue'] <= -0.004) and
                                (row['cashAtEndOfPeriod'] > -916000.0)
                            ) or
                            (
                                (row['longTermDebt'] > 1376553984.0) and
                                (row['interestExpense'] > 9500000.0) and
                                (row['priceToSalesRatio'] > 0.701) and
                                (row['interestDebtPerShare'] <= 9.185) and
                                (row['capexToDepreciation'] <= -1.146) and
                                (row['totalNonCurrentLiabilities'] > 2758150016.0) and
                                (row['workingCapital'] <= 2675240576.0) and
                                (row['capexPerShare'] > -4.358) and
                                (row['netProfitMargin'] <= 0.221) and
                                (row['tangibleAssetValue'] > -9714500096.0) and
                                (row['cashAndShortTermInvestments'] > 197049000.0) and
                                (row['operatingProfitMargin'] <= 0.419) and
                                (row['priceToSalesRatio.1'] > 0.959) and
                                (row['returnOnAssets'] <= 0.173) and
                                (row['tangibleAssetValue'] > -8444000256.0) and
                                (row['cashAndShortTermInvestments'] > 203500000.0) and
                                (row['freeCashFlowYield'] <= 0.097) and
                                (row['propertyPlantEquipmentNet'] > 778600000.0) and
                                (row['marketCap'] <= 535985684480.0)
                            ) or
                            (
                                (row['longTermDebt'] <= 1376553984.0) and
                                (row['capexToRevenue'] <= -0.003) and
                                (row['marketCap'] > 2403451136.0) and
                                (row['effectiveTaxRate'] <= 0.278) and
                                (row['longTermDebtToCapitalization'] > 0.082) and
                                (row['grahams_pb'] <= 179.518) and
                                (row['weightedAverageShsOut'] > 151144240.0) and
                                (row['cashAtEndOfPeriod'] <= 466696496.0) and
                                (row['revenuePerShare'] > 1.849) and
                                (row['depreciationAndAmortization.1'] <= 227500000.0) and
                                (row['workingCapital'] <= 1887760512.0) and
                                (row['priceEarningsToGrowthRatio'] <= 2.059) and
                                (row['returnOnTangibleAssets'] > -0.043) and
                                (row['commonStock'] <= 2571931136.0) and
                                (row['otherCurrentLiabilities'] <= 1450000000.0) and
                                (row['grahams_pe'] <= 1112.356) and
                                (row['ebitdaratio'] <= 0.525)
                            )
                    ):
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
