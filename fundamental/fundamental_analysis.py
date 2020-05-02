from urllib.request import urlopen
import json
import pandas as pd

pd.options.display.max_columns = 20
pd.options.display.max_rows = 100


def select_sector(df, sector):
    """
    :param df: takes a df containing a 'sector' column
    :param sector: takes a string representing a sector
    :return: a df containing only companies in the specified sector
    """
    print('Evaluating sector membership among ' + str(df['symbol'].nunique()) + ' companies...')

    sector_filter = df['sector'] == sector
    df = df[sector_filter]

    print('Found ' + str(len(sector_profiles)) + ' companies in the ' + sector + ' sector!')

    return df


# TODO: industry param needs to accept list of industry names
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

    clean_data = df.loc[df['date'].apply(lambda x: len(x) == 10)].copy()

    clean_data['year'] = clean_data['date'].str[:4]

    print('Returning clean financial statement data for ' + str(clean_data['symbol'].nunique()) + ' companies!')

    return clean_data


def subset_financial_statement(df, statement_year, eval_period):
    """
    :param df: takes a df with a year column
    :param statement_year: represents most recent financial statement year (e.g., 2019) required
    :param eval_period: represents number of years leading up to the statement year that we'd like to analyze
    :return: a df that is a subset of the original df provided
    """

    print('Pulling data from ' + str(statement_year - eval_period) + ' to ' + str(statement_year) + ' for '
          + str(df['symbol'].nunique()) + ' companies...')

    # Remove tickers without recent financial reports
    latest_statement = df.groupby(['symbol'])['year'].max()
    latest_statement_filter = latest_statement[latest_statement == str(statement_year)]
    recent_reporters = df[df['symbol'].isin(latest_statement_filter.index)]

    # Filter data-set for last N years
    year_filter = int(statement_year) - int(eval_period)
    recent_data = recent_reporters[(recent_reporters['year'].astype(int) >= year_filter)]

    print('Found data from ' + str(statement_year - eval_period) + ' to ' + str(statement_year) + ' for '
          + str(df['symbol'].nunique()) + ' companies!')

    return recent_data


# get all three financial statements joined together after cleaning
    # Necessary to calculate all of the category metrics listed below
    # Some metrics require numbers from more than one statement
def join_financial_statements(income_statement, balance_sheet, cash_flow_statement):
    pass

# research annual vs. quarterly reporting


# profitability
def calculate_profitability_metrics(df):
    pass
# Takes in the joined financial statements df
# Returns a separate profitability metrics df

# liquidity

# solvency

# cash flow

# activity


# FOR EACH COLUMN SELECTED: pivot and calculate ttm and 1, 3, 5 year growth rates and then unpivot / transpose
def calculate_metric_growth(df):
    pass
# Takes in profitability metrics (or other) df
# Returns profitability metrics df with new growth columns


def join_metrics(profitability, liquidity, solvency, cashflow, activity):
    pass


def filter_companies_on_metrics(df):
    pass


companies = pd.read_csv('company_profiles.csv')
sect = select_sector(companies, 'Consumer Defensive')
ind = select_industry(sect, 'Consumer Packaged Goods')
income_statement_annual = get_financial_statement(ind, 'income-statement', 'annual')
income_statement_clean = clean_financial_statement(income_statement_annual)
income_statement_subset = subset_financial_statement(income_statement_clean, 2019, 5)
print(income_statement_subset)