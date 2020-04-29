from urllib.request import urlopen
import json
import pandas as pd

# Set global printing options
pd.options.display.max_columns = 20
pd.options.display.max_rows = 100


def filter_exchanges(df):
    """
    :param df: takes a df containing an 'exchange' column
    :return: a df containing only companies listed on the specified exchanges
    """
    exchange_list = ['Nasdaq Global Select', 'NasdaqGS', 'Nasdaq', 'New York Stock Exchange', 'NYSE', 'NYSE American']
    exchange_filter = df[df['exchange'].isin(exchange_list)]

    return exchange_filter


def select_sector(df, sector):
    """
    :param df: takes a df containing a 'sector' column
    :param sector: takes a string representing a sector
    :return: a df containing only companies in the specified sector
    """
    print('Evaluating sector membership among ' + str(df['symbol'].nunique()) + ' companies...')

    sector_filter = df['sector'] == sector
    sector_profiles = df[sector_filter]

    print('Found ' + str(len(sector_profiles)) + ' companies in the ' + sector + ' sector!')

    return sector_profiles


def select_industry(df, industry):
    """
    :param df: takes a df containing a 'industry' column
    :param industry: takes a string representing an industry
    :return: a df containing only companies in the specified industry
    """
    print('Evaluating industry membership among ' + str(df['symbol'].nunique()) + ' companies...')

    industry_filter = df['industry'] == industry
    industry_profiles = df[industry_filter]

    print('Found ' + str(len(industry_profiles)) + ' companies in the ' + industry + ' industry!')

    return industry_profiles


def get_financial_ratios(df):
    """
    :param df: takes a df containing a "symbol" (stock ticker) column as input
    :return: a df of financial ratios for every symbol (stock ticker) with available data
    """
    print('Pulling financial ratios for ' + str(df['symbol'].nunique()) + ' companies...')

    financial_ratios = pd.DataFrame()

    for ticker in df['symbol']:
        response = urlopen("https://financialmodelingprep.com/api/v3/financial-ratios/" + ticker)
        data = response.read().decode("utf-8")

        # Select stock tickers don't return any results - appears to be tickers that include a "."
        try:
            data_json = json.loads(data)['ratios']
            flattened_data = pd.json_normalize(data_json)
            flattened_data.insert(0, 'stock.symbol', ticker)
            financial_ratios = financial_ratios.append(flattened_data, ignore_index=True)

        except KeyError:
            continue

    financial_ratios.columns = financial_ratios.columns.str.split('.').str[1]
    financial_ratios.columns.values[1] = "date"

    print('Found financial ratio data for ' + str(financial_ratios['symbol'].nunique()) + ' companies!')

    return financial_ratios


def get_financial_statement(df, statement, period):
    """
    :param df: takes a df with a symbol (ticker) column
    :param statement: requires one of: income-statement, balance-sheet, or cash-flow-statement
    :param period: requires on of: annual, quarterly
    :return: a df containing all financial statement data
    """

    print('Pulling ' + str(statement) + ' data for ' + str(df['symbol'].nunique()) + ' companies...')

    financial_statement = pd.DataFrame()

    for ticker in df['symbol']:
        response = urlopen("https://financialmodelingprep.com/api/v3/financials/" + statement + "/" + ticker
                           + "?period=" + period)
        data = response.read().decode("utf-8")

        try:
            data_json = json.loads(data)['financials']
            flattened_data = pd.json_normalize(data_json)
            flattened_data.insert(0, 'symbol', ticker)
            financial_statement = financial_statement.append(flattened_data, ignore_index=True)

        except KeyError:
            continue

    print('Found ' + str(statement) + ' data for ' + str(financial_statement['symbol'].nunique()) + ' companies!')

    return financial_statement


def clean_financial_statement(df):
    """
    :param df: a df containing financial statement data (income, balance, or cash flow statement)
    :return: a df with clean financial statement data (corrupted "date" rows removed, year column added)
    """
    print('Cleaning financial statement data for ' + str(df['symbol'].nunique()) + ' companies...')

    # Remove rows without full dates
    clean_data = df.loc[df['date'].apply(lambda x: len(x) == 10)].copy()

    # Create year column
    clean_data['year'] = clean_data['date'].str[:4]

    print('Returning clean financial statement data for ' + str(clean_data['symbol'].nunique()) + ' companies!')

    return clean_data


#
#
# def select_last_n_years(df, most_recent_year, years_prior):
#
#     # Remove rows without full dates
#     df = df.loc[df['date'].apply(lambda x: len(x) == 10)]
#
#     # Create year column
#     df['year'] = df['date'].str[:4].astype(int)
#
#     # Filter data-set for last N years
#     year_filter = max(df['year']) - years_prior
#     df = df[(df['year'] >= year_filter)]
#
#     # Remove tickers without recent financial reports
#     most_recent_statement = df.groupby(['symbol'])['year'].max()
#     recent_statement_filter = most_recent_statement[most_recent_statement == most_recent_year]
#
#     # Inner Join with income_statement_annual
#     clean_df = df[df['symbol'].isin(recent_statement_filter.index)]
#
#     return clean_df


companies = pd.read_csv('company_profiles.csv')
sector = select_sector(companies, 'Consumer Defensive')
ind = select_industry(sector, 'Consumer Packaged Goods')
income_statement_annual = get_financial_statement(ind, 'income-statement', 'annual')
income_statement_clean = clean_financial_statement(income_statement_annual)
print(income_statement_clean)






"""
def filter_by_ratio(df, gpm=0.0, opm=0.0, npm=0.0, roe=0.15, cr=1.5, ic=15, cfd=0.60):

    print('Evaluating the financial ratios of ' + str(df['symbol'].nunique()) + ' companies...')

    # Subset df to profitability ratios we're concerned with
    subset_cols = df[['symbol', 'date', 'grossProfitMargin', 'operatingProfitMargin', 'netProfitMargin',
                      'returnOnEquity', 'currentRatio', 'interestCoverage', 'cashFlowToDebtRatio']]

    # Subset df to latest reported profitability ratios (annual basis)
    subset_rows = subset_cols.groupby('symbol').head(1).drop_duplicates(['symbol'])

    # TODO: Change this to use index instead on column names
    # Convert ratios values to floats instead of strings
    subset_rows[['grossProfitMargin', 'operatingProfitMargin', 'netProfitMargin', 'returnOnEquity', 'currentRatio',
                 'interestCoverage', 'cashFlowToDebtRatio']]\
        = subset_rows[['grossProfitMargin', 'operatingProfitMargin', 'netProfitMargin', 'returnOnEquity', 'currentRatio',
                       'interestCoverage', 'cashFlowToDebtRatio']].apply(pd.to_numeric)

    # Filter out companies with negative GPM, OPM, or NPM
    keeper_stocks = subset_rows[(subset_rows['grossProfitMargin'] > gpm)
                                & (subset_rows['operatingProfitMargin'] > opm)
                                & (subset_rows['netProfitMargin'] > npm)
                                & (subset_rows['returnOnEquity'] > roe)
                                & (subset_rows['currentRatio'] > cr)
                                & (subset_rows['interestCoverage'] > ic)
                                & (subset_rows['cashFlowToDebtRatio'] > cfd)]

    profitable_companies = pd.merge(left=df, right=keeper_stocks['symbol'], left_on='symbol', right_on='symbol')

    print('Found ' + str(profitable_companies['symbol'].nunique()) +
          ' companies that meet your requirements!')

    return profitable_companies
"""