from urllib.request import urlopen
import json
import pandas as pd

pd.options.display.max_columns = 20
pd.options.display.max_rows = 100


def select_sector(df, *args):
    """
    Remove companies not in the sector provided.

    :param df: DataFrame containing sector info on N companies
    :param args: tuple representing sectors to retain for analysis
    :return: Subset of DataFrame provided, containing companies in the specified sector
    :rtype: pandas.DataFrame
    """
    print('Evaluating sector membership among ' + str(df['symbol'].nunique()) + ' companies...')

    sector_filter = list(args)
    df = df[df['sector'].isin(sector_filter)]

    print('Found ' + str(df['symbol'].nunique()) + ' companies in the ' + str(sector_filter)
          + ' sector! \n')

    return df


def select_industries(df, *args):
    """
    Remove companies not in the industries provided.

    :param df: DataFrame containing industry info on N companies
    :param args: tuple representing industries to retain for analysis
    :return: Subset of DataFrame provided, containing companies in the specified industry
    :rtype: pandas.DataFrame
    """
    print('Evaluating industry membership among ' + str(df['symbol'].nunique()) + ' companies...')

    industry_filter = list(args)
    df = df[df['industry'].isin(industry_filter)]

    print('Found ' + str(df['symbol'].nunique()) + ' companies in the ' + str(industry_filter)
          + ' industries! \n')

    return df


def get_financial_data(df, request, period):
    """
    Retrieve financial data for all stock tickers in the provided DataFrame.

    :param df: DataFrame containing stock tickers (symbol) for N companies
    :param request: String representing aspect of API to query
    :param period: String 'annual' or 'quarter'
    :return: DataFrame containing chosen financial data for all years available
    :rtype: pandas.DataFrame
    """
    print('Pulling ' + period + ' ' + request + ' for ' + str(df['symbol'].nunique())
          + ' companies...')

    request_map = {"financials": "financials",
                   "financial-ratios": "ratios",
                   "enterprise-value": "enterpriseValues",
                   "company-key-metrics": "metrics",
                   "financial-statement-growth": "growth"}

    value_key = request_map[request]

    financial_statements = ['income-statement', 'balance-sheet-statement', 'cash-flow-statement']

    financial_data = pd.DataFrame()

    if request == 'financials':

        for ticker in df['symbol']:

            statement_data = pd.DataFrame(df['symbol'])

            for statement in financial_statements:
                response = urlopen("https://financialmodelingprep.com/api/v3/" + request + "/" +
                                   statement + "/" + ticker + "?period=" + period)
                data = response.read().decode("utf-8")

                try:
                    data_json = json.loads(data)[value_key]

                except KeyError:
                    continue

                flattened_data = pd.json_normalize(data_json)
                flattened_data.insert(0, 'symbol', ticker)
                statement_data = statement_data.merge(flattened_data)

            financial_data = pd.concat([financial_data, statement_data], ignore_index=True)

        print('Found ' + period + ' financial statement data for '
              + str(financial_data['symbol'].nunique()) + ' companies! \n')

    else:

        for ticker in df['symbol']:
            response = urlopen("https://financialmodelingprep.com/api/v3/" + request + "/" +
                               ticker + "?period=" + period)
            data = response.read().decode("utf-8")

            try:
                data_json = json.loads(data)[value_key]

            except KeyError:
                continue

            flattened_data = pd.json_normalize(data_json)
            flattened_data.insert(0, 'symbol', ticker)
            financial_data = pd.concat([financial_data, flattened_data], ignore_index=True)

        print('Found ' + period + ' ' + request + ' data for '
              + str(financial_data['symbol'].nunique()) + ' companies! \n')

    return financial_data


def clean_financial_data(df, period):
    """
    Remove rows with corrupted date values, create new year column, remove duplicate financial
    reports for the provided period: annual = 1 report max or quarterly = 4 reports max.

    :param df: DataFrame containing financial data on N companies
    :param period: String 'annual' or 'quarter'
    :return: Subset of provided DataFrame, with the addition of a new 'year' column
    :rtype: pandas.DataFrame
    """
    print('Cleaning financial data for ' + str(df['symbol'].nunique()) + ' companies...')

    df['date'] = df['date'].astype(str)
    df = df.loc[df['date'].apply(lambda x: len(x) == 10)].copy()

    df.insert(2, 'year', df['date'].str[:4])
    df['year'] = df.year.astype(int)
    # Sort by new year column
    # If period == 'annual': LOGIC, elif period == 'quarterly': LOGIC

    print('Returning clean financial data for ' + str(df['symbol'].nunique())
          + ' companies! \n')

    return df


def select_analysis_years(df, report_year, eval_period):
    """
    Remove companies without recent financial reports or reporting history dating back to the
    evaluation period specified.

    :param df: DataFrame containing financial data on N companies
    :param report_year: year of most recent financial report
    :param eval_period: number of years prior to most recent report to be analyzed
    :return: Subset of the DataFrame provided
    :rtype: pandas.DataFrame
    """

    print('Subsetting data from ' + str(report_year - eval_period) + ' to ' + str(report_year)
          + ' for ' + str(df['symbol'].nunique()) + ' companies...')

    min_year = report_year - eval_period

    for ticker in df['symbol']:
        if df['year'].max() != report_year or df['year'].min() > min_year:
            df = df[df.symbol != ticker]

    df = df[(df['year'].astype(int) >= min_year)]

    print('Subset data from ' + str(report_year - eval_period) + ' to ' + str(report_year)
          + ' for ' + str(df['symbol'].nunique()) + ' companies! \n')

    return df


def main():
    company_profiles = pd.read_csv('data/company-profiles.csv')

    sector_companies = select_sector(company_profiles, 'Consumer Cyclical')

    request_list = ['financials', 'financial-ratios', 'financial-statement-growth',
                    'company-key-metrics', 'enterprise-value']

    for request in request_list:
        raw_data = get_financial_data(sector_companies, request, 'annual')
        clean_data = clean_financial_data(raw_data, 'annual')
        subset_data = select_analysis_years(clean_data, 2019, 10)
        filename = 'data/' + request + '.csv'
        subset_data.to_csv(filename, index=False, header=True)

    return None


if __name__ == '__main__':
    main()

