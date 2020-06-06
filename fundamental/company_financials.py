from fundamental import config
from urllib.request import urlopen

import json
import pandas as pd


def select_sector(df, *args):
    """
    Remove companies not in the sector provided.

    :param df: DataFrame containing sector info on N companies
    :param args: Sectors to retain for analysis
    :return: Subset of DataFrame provided, containing companies in the specified sector
    :rtype: pandas.DataFrame
    """
    print('Evaluating sector membership among ' + str(df['symbol'].nunique()) + ' companies...')

    sector_filter = list(args)
    df = df[df['profile.sector'].isin(sector_filter)]

    print('Found ' + str(df['symbol'].nunique()) + ' companies in the ' + str(sector_filter)
          + ' sector! \n')

    return df


def select_industries(df, *args):
    """
    Remove companies not in the industries provided.

    :param df: DataFrame containing industry info on N companies
    :param args: Industries to retain for analysis
    :return: Subset of DataFrame provided, containing companies in the specified industry
    :rtype: pandas.DataFrame
    """
    print('Evaluating industry membership among ' + str(df['symbol'].nunique()) + ' companies...')

    industry_filter = list(args)
    df = df[df['profile.industry'].isin(industry_filter)]

    print('Found ' + str(df['symbol'].nunique()) + ' companies in the ' + str(industry_filter)
          + ' industries! \n')

    return df


def get_financial_data(df, request, period, api_key):
    """
    Retrieve financial data for all stock tickers in the provided DataFrame.

    :param df: DataFrame containing stock tickers (symbol) for N companies
    :param request: String representing aspect of API to query
    :param period: String 'annual' or 'quarter'
    :param api_key: FinancialModelingPrep API key
    :return: DataFrame containing chosen financial data for all years available
    :rtype: pandas.DataFrame
    """
    print('Pulling ' + period + ' ' + request + ' for ' + str(df['symbol'].nunique())
          + ' companies...')

    request_map = {"financials": "financials",
                   "financial-ratios": "ratios",
                   "enterprise-value": "enterprise-values",
                   "company-key-metrics": "key-metrics",
                   "financial-statement-growth": "financial-growth"}

    value_key = request_map[request]

    financial_statements = ['income-statement', 'balance-sheet-statement', 'cash-flow-statement']

    financial_data = pd.DataFrame()

    if request == 'financials':

        for ticker in df['symbol']:

            statement_data = pd.DataFrame(df['symbol'])

            for statement in financial_statements:
                response = urlopen("https://financialmodelingprep.com/api/v3/" + statement + "/"
                                   + ticker + "?period=" + period + "&apikey=" + api_key)

                data = response.read().decode("utf-8")
                data_json = json.loads(data)

                flattened_data = pd.json_normalize(data_json)

                try:
                    statement_data = statement_data.merge(flattened_data, on='symbol', how='inner')

                except KeyError:
                    continue

                duplicate_cols = [x for x in statement_data if x.endswith('_x') or x.endswith('_y')]
                statement_data.drop(duplicate_cols, axis=1, inplace=True)

            financial_data = pd.concat([financial_data, statement_data], ignore_index=True)

        print('Found ' + period + ' financial statement data for '
              + str(financial_data['symbol'].nunique()) + ' companies! \n')

    else:

        for ticker in df['symbol']:
            response = urlopen("https://financialmodelingprep.com/api/v3/" + value_key + "/"
                               + ticker + "?period=" + period + "&apikey=" + api_key)

            data = response.read().decode("utf-8")
            data_json = json.loads(data)

            flattened_data = pd.json_normalize(data_json)
            financial_data = pd.concat([financial_data, flattened_data], ignore_index=True)

        print('Found ' + period + ' ' + request + ' data for '
              + str(financial_data['symbol'].nunique()) + ' companies! \n')

    return financial_data


def clean_financial_data(df):
    """
    Remove rows with corrupted date values, create new year column.

    :param df: DataFrame containing financial data on N companies
    :return: Subset of provided DataFrame, with the addition of a new 'year' column
    :rtype: pandas.DataFrame
    """
    print('Cleaning financial data for ' + str(df['symbol'].nunique()) + ' companies...')

    df = df.loc[df['date'].astype(str).apply(lambda x: len(x) == 10)].copy()

    df.insert(2, 'year', df['date'].str[:4])
    df['year'] = df.year.astype(int)

    print('Returning clean financial data for ' + str(df['symbol'].nunique()) + ' companies! \n')

    return df


def select_analysis_years(df, report_year, eval_period):
    """
    Remove companies without financial reports in the evaluation period specified.

    :param df: DataFrame containing financial data on N companies
    :param report_year: Year of most recent financial report
    :param eval_period: Number of years prior to most recent report to be analyzed
    :return: Subset of the DataFrame provided
    :rtype: pandas.DataFrame
    """

    print('Subsetting data from ' + str(report_year - eval_period) + ' to ' + str(report_year)
          + ' for ' + str(df['symbol'].nunique()) + ' companies...')

    df.sort_values(by=['symbol', 'year'], inplace=True, ascending=True)
    df.drop_duplicates(['symbol', 'year'], keep='last', inplace=True)

    start_year = report_year - eval_period

    historical_years = set()
    tickers_to_drop = []

    for i in range(start_year, report_year + 1):
        historical_years.add(i)

    symbol_history = df.groupby('symbol')['year'].apply(set)

    for symbol, year_set in enumerate(symbol_history):
        common_years = historical_years.intersection(year_set)
        if len(common_years) != len(historical_years):
            tickers_to_drop.append(symbol_history.index[symbol])
        else:
            continue

    df = df[~df['symbol'].isin(tickers_to_drop)]
    df = df[df['year'].isin(historical_years)]

    print('Subset data from ' + str(report_year - eval_period) + ' to ' + str(report_year)
          + ' for ' + str(df['symbol'].nunique()) + ' companies! \n')

    return df


# TODO: Add logic to select specific quarters for analysis
def select_analysis_quarters(df, report_year, eval_period, *args):
    pass


def main():
    company_profiles = pd.read_csv('data/company-profiles.csv')

    sector_companies = select_sector(company_profiles, 'Consumer Cyclical')

    request_list = ['financials', 'financial-ratios', 'financial-statement-growth',
                    'company-key-metrics', 'enterprise-value']

    for request in request_list:
        raw_data = get_financial_data(sector_companies, request, 'annual', config.api_key)
        clean_data = clean_financial_data(raw_data)
        subset_data = select_analysis_years(clean_data, 2019, 10)
        evaluation_period = subset_data.year.max() - subset_data.year.min()
        filename = 'data/' + request + '-' + str(evaluation_period) + 'Y' + '.csv'
        subset_data.to_csv(filename, index=False, header=True)

    return None


if __name__ == '__main__':
    main()
