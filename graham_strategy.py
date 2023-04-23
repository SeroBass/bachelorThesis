import os.path
import pandas as pd

def search_for_possibilities():
    print('Starting applying Graham')

    # Criteria:
    # (Current Ratio > 2) and
    # (total non-current liabilities < working capital or < net current asset value)
    def financial_strength(df_data):
        financial_strength_list = []
        years_list = []
        yearly_strength_dict = {}
        for index, row in df_data.iterrows():
            if int(index[0:4]) not in years_list:
                try:
                    current_ratio = df_data.loc[index]['currentRatio']
                    total_non_current_liabilities = df_data.loc[index]['totalNonCurrentLiabilities']
                    working_capital = df_data.loc[index]['workingCapital']
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

    # Criteria:
    # Positive EPS for the last 10 years
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

    # Criteria:
    # Continious dividends the last 10 years (not 20 years because not enough data)
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

    # Criteria:
    # mean EPS of last 3 years must be +33% than mean EPS of first 3 years
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

    # Calculation:
    # Today's PE-Ratio = Price / mean of the last 3 EPS
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
                pe_list.append(0)
        return pe_list

    # Calculation:
    # Today's PB-Ratio = Price / Actual Book Value per Share
    def pb(df_data):
        pb_list = []
        years_list = []
        yearly_bps_dict = {}
        for index, row in df_data.iterrows():
            if int(index[0:4]) not in years_list:
                yearly_bps_dict[int(index[0:4])] = df_data.loc[index]['bookValuePerShare']
                years_list.append(int(index[0:4]))

        for index, row in df_data.iterrows():
            try:
                pb_ratio = row['price'] / row['bookValuePerShare']
                pb_list.append(pb_ratio)
            except:
                pb_list.append(0)
        return pb_list

    # Get used tickers
    with open('data/tickers/stocks_used.txt', 'r') as f:
        text = f.readlines()
        text = [t.strip() for t in text]

    for ticker in text:
        print('Apply Graham Calculations on ', ticker)
        csv_name = str(ticker) + '.csv'
        df_data = pd.read_csv(os.path.join('data/financials/', csv_name), index_col=0)

        # Call functions for Graham evaluation
        df_data['grahams_financial_strength_decision'] = financial_strength(df_data)
        df_data['grahams_earnings_stability_decision'] = earnings_stability(df_data)
        df_data['grahams_dividend_stability_decision'] = dividend_stability(df_data)
        df_data['grahams_earnings_growth_decision'] = earnings_growth(df_data)
        df_data['grahams_pe'] = pe(df_data)
        df_data['grahams_pb'] = pb(df_data)

        # Save calculations by replacing old CSV with new CSV
        os.remove(os.path.join('data/financials/', csv_name))
        df_data.to_csv(os.path.join('data/financials/', csv_name), index=True, header=True)

    print('Finished applying Graham')


