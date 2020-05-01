from urllib.request import urlopen
import json
import pandas as pd

pd.options.display.max_columns = 20
pd.options.display.max_rows = 100


def get_company_data():
    """
    Retrieve all available company stocks from FinancialModelingPrep API.

    :return: DataFrame containing 'symbol', 'name', 'price', and 'exchange' columns
    :rtype: pandas.DataFrame
    """
    print('Retrieving stock data from FinancialModelingPrep...')

    response = urlopen("https://financialmodelingprep.com/api/v3/company/stock/list")
    data = response.read().decode("utf-8")
    data_json = json.loads(data)['symbolsList']
    flattened_data = pd.json_normalize(data_json)

    print('Found stock data on ' + str(flattened_data.symbol.nunique()) + ' companies!')

    return flattened_data


def clean_company_data(df):
    """
    Remove rows with any NaN values.

    :param df: DataFrame containing 'symbol', 'name', 'price', and 'exchange' columns
    :return: A subset of the original DataFrame
    :rtype: pandas.DataFrame
    """
    pass


def select_stock_exchanges(df):
    pass


def select_price_threshold(df, price):
    pass

# def create_company_profile(df):
#     """
#     Construct a company profile given a set of stock tickers.
#
#     Creates necessary association between stock tickers and company attributes.
#
#     :return: A DataFrame object containing select company attributes, joined with provided tickers
#     :rtype: pandas.DataFrame
#     """
#     stock_tickers = pd.read_csv('ticker_company_mapping.csv', index_col=0)
#
#     company_data = []
#
#     for ticker in stock_tickers['symbol']:
#         response = urlopen("https://financialmodelingprep.com/api/v3/company/profile/" + ticker)
#         data = response.read().decode("utf-8")
#         data_json = json.loads(data)['profile']
#         company_data.append(data_json)
#
#     company_df = pd.DataFrame(company_data)
#     company_df = company_df[['companyName', 'sector', 'industry', 'exchange', 'ceo', 'description',
#                              'website', 'mktCap', 'volAvg', 'beta', 'price']]
#     # company_df = company_df.set_index('companyName')
#
#     company_profile = company_df.merge(stock_tickers, right_index=True, left_index=True,
#                                        how='inner')
#
#     return company_profile
