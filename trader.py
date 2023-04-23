from datetime import date
import pandas as pd
import os
import os.path

# Strategy based on Graham Principles
# Target = Entry-Price * 1.5 (therefore 50% gain)
def trade_graham_50():
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
            df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
    df_transaction_history.to_csv('data/backtesting/transaction_history_graham_50.csv')
    print('Finished Backtesting')

# Strategy based on Decision Tree Classifier
# Target = Entry-Price * 1.5 (therefore 50% gain)
def trade_ml_50():
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
            # open position
            if position_is_open == 0 and (
                    ((row['longTermDebt'] <= 1376553984.0) and (row['capexToRevenue'] <= -0.003) and (row['marketCap'] <= 2403451136.0) and (row['weightedAverageShsOut'] > 36000304.0) and (row['revenue'] > 17000244.0) and (row['quickRatio'] <= 4.476) and (row['fixedAssetTurnover'] <= 240.432) and (row['marketCap'] <= 1651521152.0) and (row['grossProfitMargin'] > 0.149) and (row['propertyPlantEquipmentNet'] > 64000.0) and (row['enterpriseValueOverEBITDA'] > -34.013) and (row['capexToRevenue'] <= -0.003) and (row['priceEarningsRatio'] > -562.512) and (row['cashPerShare'] > 0.001) and (row['freeCashFlowYield'] <= 0.509) and (row['debtToAssets'] > 0.195) and (row['peRatio'] <= 519.109) and (row['enterpriseValue'] <= 2688665600.0) and (row['changeInWorkingCapital'] > -151882000.0) and (row['ebtPerEbit'] <= 2.807) and (row['capitalExpenditureCoverageRatio'] <= 38.48) and (row['pocfratio'] > -35.836) and (row['totalStockholdersEquity'] > -260950000.0) and (row['debtToAssets'] > 0.201) and (row['grahams_pe'] > -62.328) and (row['netDebt'] > -62692500.0) and (row['debtToAssets'] > 0.23) and (row['dividendPaidAndCapexCoverageRatio'] > -140.411)) or
                    ((row['longTermDebt'] <= 1376553984.0) and (row['capexToRevenue'] <= -0.003) and (row['marketCap'] <= 2403451136.0) and (row['weightedAverageShsOut'] <= 36000304.0) and (row['weightedAverageShsOut'] <= 5840261.5) and (row['otherNonCashItems'] <= 30282304.0) and (row['priceToOperatingCashFlowsRatio'] <= 106.291) and (row['fixedAssetTurnover'] <= 25.316) and (row['othertotalStockholdersEquity'] > -102131000.0) and (row['investmentsInPropertyPlantAndEquipment'] <= -3700.5) and (row['operatingCashFlowSalesRatio'] > -4.702) and (row['pbRatio'] <= 13.461) and (row['operatingCashFlowPerShare'] > -226.201) and (row['weightedAverageShsOutDil'] <= 9754175.0) and (row['capexToRevenue'] > -6.973) and (row['priceEarningsRatio'] > -99.833) and (row['grahamNetNet'] <= 1.159) and (row['commonStock'] <= 54043190.0) and (row['grahams_pb'] <= 54.375) and (row['grahamNumber'] > 0.448) and (row['freeCashFlowPerShare.1'] > -1206.759) and (row['retainedEarnings'] > -59155728.0) and (row['cashAtEndOfPeriod'] > -7575500.0)) or
                    ((row['longTermDebt'] <= 1376553984.0) and (row['capexToRevenue'] <= -0.003) and (row['marketCap'] > 2403451136.0) and (row['effectiveTaxRate'] > 0.278) and (row['incomeQuality'] <= 4.212) and (row['operatingExpenses'] > 1481706944.0) and (row['netDebt'] > -7773253376.0) and (row['roic'] <= 2.074) and (row['incomeQuality'] <= 3.768) and (row['incomeTaxExpense'] <= 11042636928.0) and (row['cashAtBeginningOfPeriod'] > -396881928.0) and (row['ebitdaratio'] <= 0.5) and (row['netChangeInCash'] > -2571929472.0) and (row['debtEquityRatio'] <= 7.001) and (row['incomeBeforeTax'] > -35350000.0) and (row['freeCashFlowYield'] <= 0.148) and (row['returnOnCapitalEmployed'] > 0.097) and (row['returnOnTangibleAssets'] <= 0.239)) or
                    ((row['longTermDebt'] > 1376553984.0) and (row['longTermDebt'] <= 11580000256.0) and (row['priceSalesRatio'] <= 0.878) and (row['totalNonCurrentAssets'] <= 39901849600.0) and (row['cashPerShare'] <= 6.232) and (row['capexToOperatingCashFlow'] <= -0.182) and (row['otherCurrentLiabilities'] <= 11395000320.0) and (row['capitalExpenditure'] <= -105200000.0) and (row['incomeQuality'] <= 206.341) and (row['capexPerShare'] <= -0.276) and (row['bookValuePerShare'] <= 17.21) and (row['grossProfit'] <= 28080869376.0) and (row['grahams_pb'] <= 229.366) and (row['ebtPerEbit'] <= 2.319) and (row['priceEarningsToGrowthRatio'] <= 0.745) and (row['ebtPerEbit'] <= 1.162) and (row['priceEarningsRatio'] > -55.241)) or
                    ((row['longTermDebt'] <= 1376553984.0) and (row['capexToRevenue'] <= -0.003) and (row['marketCap'] <= 2403451136.0) and (row['weightedAverageShsOut'] > 36000304.0) and (row['revenue'] > 17000244.0) and (row['quickRatio'] <= 4.476) and (row['fixedAssetTurnover'] <= 240.432) and (row['marketCap'] > 1651521152.0) and (row['grahams_pe'] <= 4811.796) and (row['roic'] > -0.019) and (row['netCashUsedProvidedByFinancingActivities'] > -482900000.0) and (row['capexToOperatingCashFlow'] > -6.087) and (row['grahams_pb'] <= 1137.269) and (row['grossProfitMargin'] > 0.208) and (row['tangibleBookValuePerShare'] > -18.228) and (row['cashFlowToDebtRatio'] > -2.114) and (row['otherCurrentLiabilities'] > 30785500.0) and (row['epsdiluted'] <= 4.25) and (row['netDebtToEBITDA'] > -2.759) and (row['grahams_pe'] <= 4616.094) and (row['grahams_pe'] > -1.344594693752619e+18) and (row['capexToOperatingCashFlow'] <= -0.035) and (row['epsdiluted'] <= 2.95) and (row['workingCapital'] <= 1477454528.0) and (row['grahams_pb'] <= 1064.765) and (row['grahams_pe'] <= 4348.078) and (row['netDebt'] <= 1668121536.0) and (row['otherFinancingActivites'] <= 248890208.0) and (row['otherCurrentLiabilities'] > 38137500.0) and (row['otherInvestingActivites'] > -540493488.0)) or
                    ((row['longTermDebt'] <= 1376553984.0) and (row['capexToRevenue'] <= -0.003) and (row['marketCap'] > 2403451136.0) and (row['effectiveTaxRate'] > 0.278) and (row['incomeQuality'] <= 4.212) and (row['operatingExpenses'] <= 1481706944.0) and (row['companyEquityMultiplier'] > 1.607) and (row['retainedEarnings'] > -1094294912.0) and (row['otherCurrentLiabilities'] <= 858100000.0) and (row['evToSales'] <= 17.027) and (row['grahams_pb'] <= 13.573) and (row['operatingExpenses'] <= 1456436992.0) and (row['othertotalStockholdersEquity'] > -1078800000.0) and (row['capexPerShare'] > -6.482) and (row['marketCap'] > 2417247488.0) and (row['grahams_pe'] <= 363.5) and (row['netIncome'] > -140416024.0) and (row['netDebtToEBITDA'] <= 2.821) and (row['grahams_pb'] <= 12.944) and (row['otherNonCurrentLiabilities'] > -1090350016.0) and (row['netDebt'] <= 1357382016.0) and (row['grahams_pb'] <= 11.516) and (row['capexPerShare'] > -6.253)) or
                    ((row['longTermDebt'] > 1376553984.0) and (row['longTermDebt'] <= 11580000256.0) and (row['priceSalesRatio'] > 0.878) and (row['weightedAverageShsOutDil'] > 247146672.0) and (row['capexToDepreciation'] <= -1.131) and (row['totalNonCurrentLiabilities'] > 2756499968.0) and (row['propertyPlantEquipmentNet'] <= 52000499712.0) and (row['netIncomeRatio'] <= 0.229) and (row['cashRatio'] <= 0.921) and (row['quickRatio'] > 0.063) and (row['marketCap'] > 2988759552.0) and (row['companyEquityMultiplier'] > 1.629) and (row['tangibleAssetValue'] > -9714500096.0) and (row['otherNonCurrentAssets'] > -3622853632.0) and (row['shareholdersEquityPerShare'] <= 37.884) and (row['currentRatio'] <= 3.214) and (row['grahams_pe'] <= 5787.269) and (row['operatingProfitMargin'] <= 0.225) and (row['tangibleAssetValue'] > -8444000256.0) and (row['evToFreeCashFlow'] > -1650.355) and (row['quickRatio'] > 0.07) and (row['roic'] <= 0.27) and (row['capitalExpenditure'] <= -136000000.0) and (row['tangibleBookValuePerShare'] > -8.558) and (row['incomeQuality'] > -15.459)) or
                    ((row['longTermDebt'] <= 1376553984.0) and (row['capexToRevenue'] <= -0.003) and (row['marketCap'] <= 2403451136.0) and (row['weightedAverageShsOut'] <= 36000304.0) and (row['weightedAverageShsOut'] > 5840261.5) and (row['operatingIncomeRatio'] > 0.058) and (row['earningsYield'] > 0.056) and (row['interestExpense'] > -368000.0) and (row['weightedAverageShsOut'] > 6448766.5) and (row['capexToRevenue'] > -0.771) and (row['bookValuePerShare'] <= 273.002) and (row['tangibleAssetValue'] > -3619500.0) and (row['commonStock'] <= 767650016.0) and (row['debtEquityRatio'] <= 2.919) and (row['pfcfRatio'] <= 41.055) and (row['totalLiabilities'] <= 1651049984.0) and (row['operatingCashFlowPerShare.1'] > -12.047) and (row['cashRatio'] <= 2.998) and (row['operatingExpenses'] <= 1164399968.0) and (row['assetTurnover'] <= 3.11) and (row['cashAtEndOfPeriod'] > -916000.0) and (row['effectiveTaxRate'] <= 0.457)) or
                    ((row['longTermDebt'] <= 1376553984.0) and (row['capexToRevenue'] <= -0.003) and (row['marketCap'] > 2403451136.0) and (row['effectiveTaxRate'] <= 0.278) and (row['grahams_pb'] <= 190.825) and (row['longTermDebt'] > 11882000.0) and (row['capexToOperatingCashFlow'] <= -0.113) and (row['operatingExpenses'] <= 1593022016.0) and (row['grahamNetNet'] > -5.377) and (row['grossProfit'] > 500293504.0) and (row['totalOtherIncomeExpensesNet'] > -148000000.0) and (row['dividendPaidAndCapexCoverageRatio'] <= 5.092) and (row['investedCapital'] > 0.018) and (row['totalCurrentLiabilities'] <= 3565836032.0) and (row['quickRatio'] > 0.089) and (row['grahams_pb'] <= 180.569) and (row['priceCashFlowRatio'] <= 107.393) and (row['grahams_pb'] <= 179.212)) or
                    ((row['longTermDebt'] <= 1376553984.0) and (row['capexToRevenue'] <= -0.003) and (row['marketCap'] <= 2403451136.0) and (row['weightedAverageShsOut'] > 36000304.0) and (row['revenue'] > 17000244.0) and (row['quickRatio'] <= 4.476) and (row['fixedAssetTurnover'] <= 240.432) and (row['marketCap'] <= 1651521152.0) and (row['grossProfitMargin'] > 0.149) and (row['propertyPlantEquipmentNet'] > 64000.0) and (row['enterpriseValueOverEBITDA'] > -34.013) and (row['capexToRevenue'] <= -0.003) and (row['priceEarningsRatio'] > -562.512) and (row['cashPerShare'] > 0.001) and (row['freeCashFlowYield'] <= 0.509) and (row['debtToAssets'] > 0.195) and (row['peRatio'] <= 519.109) and (row['enterpriseValue'] <= 2688665600.0) and (row['changeInWorkingCapital'] > -151882000.0) and (row['ebtPerEbit'] <= 2.807) and (row['capitalExpenditureCoverageRatio'] <= 38.48) and (row['pocfratio'] > -35.836) and (row['totalStockholdersEquity'] > -260950000.0) and (row['debtToAssets'] > 0.201) and (row['grahams_pe'] > -62.328) and (row['netDebt'] <= -62692500.0) and (row['grahams_pe'] <= 3801.735) and (row['priceToFreeCashFlowsRatio'] <= 137.943) and (row['grahams_pe'] <= 3796.269) and (row['ebtPerEbit'] > -5.278) and (row['ebitda'] <= 1196395008.0))
            ):
                print('Hello')
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
                'holding_days': date(int(last_day[0:4]), int(last_day[5:7]), int(last_day[8:10])) - date(int(entry_date[0:4]), int(entry_date[5:7]), int(entry_date[8:10])), 'pnl (%)': (100 / entry_price * last_price) - 100
            })
            df_transaction_history = pd.concat([df_transaction_history, new_position.to_frame().T], ignore_index=True)
    df_transaction_history.to_csv('data/backtesting/transaction_history_ml_50.csv')
    print('Finished Backtesting ML')
