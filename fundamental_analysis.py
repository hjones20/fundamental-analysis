from urllib.request import urlopen
import json
import FundamentalAnalysis as fa
import pandas as pd

# Set global printing options
pd.options.display.max_columns = 20
pd.options.display.max_rows = 100

# Fetch the available company profiles
company_profiles = pd.read_csv('company_profiles.csv')


# ---------------------------------
# Select your circle of competence
# ---------------------------------
def select_sector(df, sector):
    sector_filter = df['sector'] == sector
    sector_profiles = df[sector_filter]
    print('Found ' + str(len(sector_profiles)) + ' companies in the ' + sector + ' sector!')
    return sector_profiles


tech_companies = select_sector(company_profiles, 'Technology')


def select_industry(df, industry):
    industry_filter = df['industry'] == industry
    industry_profiles = df[industry_filter]
    print('Found ' + str(len(industry_profiles)) + ' companies in the ' + industry + ' industry!')
    return industry_profiles


# ---------------------------------
# Filter #1: Profitability Ratios
# ---------------------------------

# Create function to fetch profitability ratios directly from Financial Modeling Prep API

def get_financial_ratios(df):
    """
    :param df: takes a df containing a "symbol" column as input
    :return: returns a df of financial ratios for every symbol (stock ticker) with available data
    """

    print('Looking for financial ratios for ' + str(len(df)) + ' companies...')
    financial_ratios = pd.DataFrame()

    for ticker in df['symbol']:
        response = urlopen("https://financialmodelingprep.com/api/v3/financial-ratios/" + ticker)
        data = response.read().decode("utf-8")
        # Select stock tickers don't return any results - appears to be tickers that include a "."
        try:
            data_json = json.loads(data)['ratios']
            flattened_data = pd.json_normalize(data_json)
            flattened_data.insert(0, 'ticker', ticker)
            financial_ratios = financial_ratios.append(flattened_data, ignore_index=True)
        except KeyError:
            continue

    print('Found financial ratio data for ' + str(len(financial_ratios)) + ' companies!')

    return financial_ratios


test = get_financial_ratios(tech_companies)



# Filter out companies with negative GPM, OPM, or NPM in 2019

# Create function to filter based on profitability ratios
# def profitability_filter(df):
#     print('Looking for positive GPM, OPM, and NPM ratios among ' + str(len(tech_companies)) + ' companies...')
#     positive_ratio_companies = []
#     for ticker in df['symbol']:
#         results = fa.financial_ratios(ticker)
#         subset_year = results.iloc[:,0]
#         subset_ratios = subset_year.loc[['grossProfitMargin', 'operatingProfitMargin', 'netProfitMargin']]
#         for ratio in subset_ratios:
#             if float(ratio) < 0.0:
#                 continue
#             else:
#                 positive_ratio_companies.append(ticker)
#     print('Found ' + str(len(positive_ratio_companies)) + ' companies with positive profitability ratios')
#     return positive_ratio_companies




# ---------------------------------
# Filter #2: Earnings Manipulation
# ---------------------------------

