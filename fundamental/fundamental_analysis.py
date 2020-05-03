from urllib.request import urlopen
import json
import pandas as pd

pd.options.display.max_columns = 20
pd.options.display.max_rows = 100


def get_financial_statement(df, statement, period):
    """
    Retrieve financial statement data for all stock tickers in the provided DataFrame

    :param df: DataFrame containing a 'symbol' column
    :param statement: String 'income-statement', 'balance-sheet-statement', or 'cash-flow-statement'
    :param period: String 'annual' or 'quarter'
    :return: DataFrame containing chosen financial statement data for all years available
    :rtype: pandas.DataFrame
    """

    print('Pulling ' + str(statement) + ' data for ' + str(df['symbol'].nunique())
          + ' companies...')

    financial_statement = pd.DataFrame()

    for ticker in df['symbol']:
        response = urlopen("https://financialmodelingprep.com/api/v3/financials/" + statement
                           + "/" + ticker + "?period=" + period)
        data = response.read().decode("utf-8")

        try:
            data_json = json.loads(data)['financials']
            flattened_data = pd.json_normalize(data_json)
            flattened_data.insert(0, 'symbol', ticker) # Change append to concat
            financial_statement = financial_statement.append(flattened_data, ignore_index=True)

        except KeyError:
            continue

    print('Found ' + str(statement) + ' data for ' + str(financial_statement['symbol'].nunique())
          + ' companies!')

    return financial_statement


def clean_financial_statement(df):
    """
    Remove rows with corrupted date values, create new year column

    :param df: DataFrame containing financial statement data
    :return: Subset of the original DataFrame, with the addition of a new 'year' column
    :rtype: pandas.DataFrame
    """
    print('Cleaning financial statement data for ' + str(df['symbol'].nunique()) + ' companies...')

    clean_data = df.loc[df['date'].apply(lambda x: len(x) == 10)].copy()

    clean_data['year'] = clean_data['date'].str[:4]

    print('Returning clean financial statement data for ' + str(clean_data['symbol'].nunique())
          + ' companies!')

    return clean_data


def select_statement_years(df, statement_year, eval_period):
    """
    Remove companies without recent financial statements, subset data to evaluation period provided.

    :param df: DataFrame containing financial statement data
    :param statement_year: year of most recent financial statement
    :param eval_period: number of years prior to most recent statement to be analyzed
    :return: Subset of the DataFrame provided
    :rtype: pandas.DataFrame
    """

    print('Pulling data from ' + str(statement_year - eval_period) + ' to ' + str(statement_year)
          + ' for ' + str(df['symbol'].nunique()) + ' companies...')

    # Remove tickers without recent financial reports (move to clean function)
    latest_statement = df.groupby(['symbol'])['year'].max()
    latest_statement_filter = latest_statement[latest_statement == str(statement_year)]
    recent_reporters = df[df['symbol'].isin(latest_statement_filter.index)]

    # Filter data-set for last N years
    year_filter = int(statement_year) - int(eval_period)
    recent_data = recent_reporters[(recent_reporters['year'].astype(int) >= year_filter)]

    print('Found data from ' + str(statement_year - eval_period) + ' to ' + str(statement_year)
          + ' for ' + str(df['symbol'].nunique()) + ' companies!')

    return recent_data


def join_financial_statements(income_statement, balance_sheet, cash_flow_statement):
    pass


def main():
    company_profiles = pd.read_csv('data/company_profiles.csv')
    print(company_profiles.head())


if __name__ == '__main__':
    main()
