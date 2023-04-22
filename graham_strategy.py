import os.path
import pandas as pd

def search_for_possibilities():
    print('Starting applying Graham')

    def company_size(df_data):
        company_size_list = []
        for index, row in df_data.iterrows():
            try:
                if df_data.loc[index]['marketCap'] - 2000000000 > 0:
                    company_size_list.append(1)
                else:
                    company_size_list.append(-1)
            except:
                company_size_list.append(-1)
        return company_size_list

    def financial_strength(df_data):
        financial_strength_list = []
        years_list = []
        yearly_strength_dict = {}
        for index, row in df_data.iterrows():
            if int(index[0:4]) not in years_list:
                try:
                    #total_current_asset = df_data.loc[index]['totalCurrentAssets']
                    #total_current_liabilities = df_data.loc[index]['totalCurrentLiabilities']
                    current_ratio = df_data.loc[index]['currentRatio']
                    cash_and_equiv = df_data.loc[index]['cashAndCashEquivalents']
                    total_non_current_liabilities = df_data.loc[index]['totalNonCurrentLiabilities']
                    working_capital = df_data.loc[index]['workingCapital']
                    #net_current_asset = total_current_asset - cash_and_equiv - total_current_liabilities
                    net_current_asset_value = df_data.loc[index]['netCurrentAssetValue']

                    if (
                            current_ratio >= 2 and
                            (
                                    total_non_current_liabilities < working_capital or
                                    total_non_current_liabilities < net_current_asset_value
                            )
                    ):
                        yearly_strength_dict[int(index[0:4])] = 1
                        years_list.append(int(index[0:4]))
                    else:
                        yearly_strength_dict[int(index[0:4])] = -1
                        years_list.append(int(index[0:4]))
                except:
                    yearly_strength_dict[int(index[0:4])] = 0
                    years_list.append(int(index[0:4]))

        for index, row in df_data.iterrows():
            year = int(index[0:4])
            financial_strength_list.append(int(yearly_strength_dict[year]))
        return financial_strength_list

    def earnings_stability(df_data):
        earnings_stability_list = []
        years_list = []
        yearly_eps_dict = {}
        for index, row in df_data.iterrows():
            if int(index[0:4]) not in years_list:
                yearly_eps_dict[int(index[0:4])] = df_data.loc[index]['eps']
                years_list.append(int(index[0:4]))

        for index, row in df_data.iterrows():
            year = int(index[0:4])
            i = 0
            eps_is_positive = 0
            try:
                while i < 10:
                    if yearly_eps_dict[year - i] > 0:
                        eps_is_positive = eps_is_positive + 1
                    i = i + 1
                if eps_is_positive == 10:
                    earnings_stability_list.append(1)
                else:
                    earnings_stability_list.append(-1)
            except:
                earnings_stability_list.append(0)
        return earnings_stability_list

    def dividend_stability(df_data):
        dividend_stability_list = []
        years_list = []
        yearly_divs_dict = {}
        for index, row in df_data.iterrows():
            if int(index[0:4]) not in years_list:
                yearly_divs_dict[int(index[0:4])] = df_data.loc[index]['dividendsPaid']
                years_list.append(int(index[0:4]))

        for index, row in df_data.iterrows():
            year = int(index[0:4])
            i = 0
            div_is_paid = 0
            try:
                while i < 10:
                    if yearly_divs_dict[year - i] < 0:
                        div_is_paid = div_is_paid + 1
                    i = i + 1
                if div_is_paid == 10:
                    dividend_stability_list.append(1)
                else:
                    dividend_stability_list.append(-1)
            except:
                dividend_stability_list.append(0)
        return dividend_stability_list

    def earnings_growth(df_data):
        earnings_growth_list = []
        years_list = []
        yearly_eps_dict = {}
        for index, row in df_data.iterrows():
            if int(index[0:4]) not in years_list:
                yearly_eps_dict[int(index[0:4])] = df_data.loc[index]['eps']
                years_list.append(int(index[0:4]))

        for index, row in df_data.iterrows():
            year = int(index[0:4])
            try:
                eps_start = (yearly_eps_dict[year] + yearly_eps_dict[year - 1] + yearly_eps_dict[year - 2]) / 3
                eps_end = (yearly_eps_dict[year - 10] + yearly_eps_dict[year - 9] + yearly_eps_dict[year - 8]) / 3
                if 100 / eps_end * eps_start > 133.33:
                    earnings_growth_list.append(1)
                else:
                    earnings_growth_list.append(-1)
            except:
                earnings_growth_list.append(0)
        return earnings_growth_list

    def pe(df_data):
        pe_list = []
        years_list = []
        yearly_eps_dict = {}
        for index, row in df_data.iterrows():
            if int(index[0:4]) not in years_list:
                yearly_eps_dict[int(index[0:4])] = df_data.loc[index]['eps']
                years_list.append(int(index[0:4]))

        for index, row in df_data.iterrows():
            year = int(index[0:4])
            try:
                pe_ratio = row['price']/((yearly_eps_dict[year] + yearly_eps_dict[year - 1] + yearly_eps_dict[year - 2]) / 3)
                pe_list.append(pe_ratio)
            except:
                pe_list.append(-1)
        return pe_list

    def pb(df_data):
        pb_list = []
        years_list = []
        yearly_bps_dict = {}
        for index, row in df_data.iterrows():
            if int(index[0:4]) not in years_list:
                yearly_bps_dict[int(index[0:4])] = df_data.loc[index]['eps']
                years_list.append(int(index[0:4]))

        for index, row in df_data.iterrows():
            year = int(index[0:4])
            try:
                pb_ratio = row['price'] / row['bookValuePerShare']
                pb_list.append(pb_ratio)
            except:
                pb_list.append(-1)
        return pb_list

    def is_buy(df_data):
        is_buy_list = []
        for index, row in df_data.iterrows():
            if (
                    int(row['grahams_company_size_decision']) == 1 and
                    int(row['grahams_financial_strength_decision']) == 1 and
                    int(row['grahams_earnings_stability_decision']) == 1 and
                    int(row['grahams_dividend_stability_decision']) == 1 and
                    int(row['grahams_earnings_growth_decision']) == 1 and
                    int(row['grahams_pe_pb_decision']) == 1
            ):
            #if row['company_size'] == 1 and row['pe_pb'] == 1 and row['dividend_stability'] == 1:
                is_buy_list.append(1)
            else:
                is_buy_list.append(0)
        return is_buy_list

    with open('data/tickers/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        csv_name = str(ticker) + '.csv'
        df_data = pd.read_csv(os.path.join('data/financials/', csv_name), index_col=0)

        #df_data['grahams_company_size_decision'] = company_size(df_data)
        df_data['grahams_financial_strength_decision'] = financial_strength(df_data)
        df_data['grahams_earnings_stability_decision'] = earnings_stability(df_data)
        df_data['grahams_dividend_stability_decision'] = dividend_stability(df_data)
        df_data['grahams_earnings_growth_decision'] = earnings_growth(df_data)
        df_data['grahams_pe'] = pe(df_data)
        df_data['grahams_pb'] = pb(df_data)

        os.remove(os.path.join('data/financials/', csv_name))
        df_data.to_csv(os.path.join('data/financials/', csv_name), index=True, header=True)
        #df_data['grahams_is_buy_decision'] = is_buy(df_data)
    print('Finished applying Graham')


