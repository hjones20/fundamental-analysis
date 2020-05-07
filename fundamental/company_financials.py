from urllib.request import urlopen
import json
import pandas as pd

pd.options.display.max_columns = 20
pd.options.display.max_rows = 100


def select_sector(df, sector):
    """
    Remove companies not in the sector provided.

    :param df: DataFrame containing sector info on N companies
    :param sector: string representing a sector (e.g., 'Consumer Defensive')
    :return: Subset of DataFrame provided, containing companies in the specified sector
    :rtype: pandas.DataFrame
    """
    print('Evaluating sector membership among ' + str(df['symbol'].nunique()) + ' companies...')

    sector_filter = df['sector'] == sector
    df = df[sector_filter]

    print('Found ' + str(df['symbol'].nunique()) + ' companies in the ' + sector + ' sector! \n')

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


def get_financial_statement(df, statement, period):
    """
    Retrieve financial statement data for all stock tickers in the provided DataFrame.

    :param df: DataFrame containing stock tickers (symbol) for N companies
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
        data_json = json.loads(data)['financials']

        try:
            flattened_data = pd.json_normalize(data_json)
            flattened_data.insert(0, 'symbol', ticker)
            financial_statement = pd.concat([financial_statement, flattened_data],
                                            ignore_index=True)

        except KeyError:
            continue

    print('Found ' + str(statement) + ' data for ' + str(financial_statement['symbol'].nunique())
          + ' companies! \n')

    return financial_statement


def clean_financial_statement(df):
    """
    Remove rows with corrupted date values, create new year column.

    :param df: DataFrame containing financial statement data on N companies
    :return: Subset of provided DataFrame, with the addition of a new 'year' column
    :rtype: pandas.DataFrame
    """
    print('Cleaning financial statement data for ' + str(df['symbol'].nunique()) + ' companies...')

    df = df.loc[df['date'].apply(lambda x: len(x) == 10)].copy()

    df['year'] = df['date'].str[:4]

    print('Returning clean financial statement data for ' + str(df['symbol'].nunique())
          + ' companies! \n')

    return df


def select_statement_years(df, statement_year, eval_period):
    """
    Remove companies without recent financial statements, subset data to evaluation period provided.

    :param df: DataFrame containing financial statement data on N companies
    :param statement_year: year of most recent financial statement
    :param eval_period: number of years prior to most recent statement to be analyzed
    :return: Subset of the DataFrame provided
    :rtype: pandas.DataFrame
    """

    print('Pulling data from ' + str(statement_year - eval_period) + ' to ' + str(statement_year)
          + ' for ' + str(df['symbol'].nunique()) + ' companies...')

    latest_statement = df.groupby(['symbol'])['year'].max()
    latest_statement_filter = latest_statement[latest_statement == str(statement_year)]
    df = df[df['symbol'].isin(latest_statement_filter.index)]

    year_filter = statement_year - eval_period
    df = df[(df['year'].astype(int) >= year_filter)]

    df = df.drop(['year'], axis=1)

    print('Found data from ' + str(statement_year - eval_period) + ' to ' + str(statement_year)
          + ' for ' + str(df['symbol'].nunique()) + ' companies! \n')

    return df


def join_financial_statements(income_statement, balance_sheet, cash_flow_statement):
    """
    Join financial statement data for all stock tickers provided, write to csv.

    :param income_statement: DataFrame containing income statement data on N companies
    :param balance_sheet: DataFrame containing balance sheet data on N companies
    :param cash_flow_statement: DataFrame containing cash flow statement data on N companies
    :return: DataFrame with the three provided financial statements inner joined
    :rtype: pandas.DataFrame
    """
    print('Joining the income, balance sheet, and cash-flow statements for ' +
          str(income_statement.symbol.nunique()) + ' companies...')

    joined = income_statement.merge(balance_sheet, how='inner', on=['symbol', 'date']).merge(
        cash_flow_statement, how='inner', on=['symbol', 'date'])

    print('Successfully joined financial statements for ' + str(joined.symbol.nunique())
          + ' companies! \n')

    joined.to_csv('data/company_financials.csv', index=False, header=True)

    return joined


# TODO: Refactor with a class (every company HAS an industry, sector, financial statements, etc.)
def main():
    company_profiles = pd.read_csv('data/company_profiles.csv')

    sector_companies = select_sector(company_profiles, 'Consumer Defensive')
    industry_companies = select_industries(sector_companies, 'Consumer Packaged Goods',
                                           'Beverages - Non-Alcoholic')

    income_statement = get_financial_statement(industry_companies, 'income-statement', 'annual')
    balance_sheet = get_financial_statement(industry_companies, 'balance-sheet-statement', 'annual')
    cashflow_statement = get_financial_statement(industry_companies, 'cash-flow-statement',
                                                 'annual')

    clean_income_statement = clean_financial_statement(income_statement)
    clean_balance_sheet = clean_financial_statement(balance_sheet)
    clean_cashflow_statement = clean_financial_statement(cashflow_statement)

    subset_income_statement = select_statement_years(clean_income_statement, 2019, 5)
    subset_balance_sheet = select_statement_years(clean_balance_sheet, 2019, 5)
    subset_cashflow_statement = select_statement_years(clean_cashflow_statement, 2019, 5)

    joined_statements = join_financial_statements(subset_income_statement, subset_balance_sheet,
                                                  subset_cashflow_statement)

    return joined_statements


if __name__ == '__main__':
    main()
