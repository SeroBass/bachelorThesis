import time

import FundamentalAnalysis as fa
import requests
from urllib.request import urlopen
import json
import pandas as pd
import csv

ticker = "IBM"
api_key = "8b7b2301a41406dc331928f7bd7e1cac"

# Show the available companies
#companies = fa.available_companies(api_key)

# Collect general company information
#profile = fa.profile(ticker, api_key)

# Collect recent company quotes
#quotes = fa.quote(ticker, api_key)

# Collect market cap and enterprise value
#entreprise_value = fa.enterprise(ticker, api_key)

# Show recommendations of Analysts
#ratings = fa.rating(ticker, api_key)

# Obtain DCFs over time
#dcf_annually = fa.discounted_cash_flow(ticker, api_key, period="annual")

# Collect the Balance Sheet statements
#balance_sheet_annually = fa.balance_sheet_statement(ticker, api_key, period="annual")

# Collect the Income Statements
#income_statement_annually = fa.income_statement(ticker, api_key, period="annual")

# Collect the Cash Flow Statements
#cash_flow_statement_annually = fa.cash_flow_statement(ticker, api_key, period="annual")

# Show Key Metrics
#key_metrics_annually = fa.key_metrics(ticker, api_key, period="annual")

# Show a large set of in-depth ratios
#financial_ratios_annually = fa.financial_ratios(ticker, api_key, period="annual")

# Show the growth of the company
#growth_annually = fa.financial_statement_growth(ticker, api_key, period="annual")

# Download general stock data
#stock_data = fa.stock_data(ticker, period="ytd", interval="1d")

# Download detailed stock data
#stock_data_detailed = fa.stock_data_detailed(ticker, api_key, begin="2000-01-01", end="2020-01-01")

# Download dividend history
#dividends = fa.stock_dividend(ticker, api_key, begin="2000-01-01", end="2020-01-01")


#print(stock_data)



