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

    print('Found ' + str(df['symbol'].nunique()) + ' companies in the ' + sector + ' sector!')

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


# profitability
def calculate_profitability_metrics(df):
    pass
# Takes in the joined financial statements df
# Returns a separate profitability metrics df

# liquidity

# solvency

# cash flow

# activity

# FOR EACH COLUMN SELECTED: pivot and calculate ttm and 1, 3, 5 year growth rates and then
# unpivot / transpose


def calculate_metric_growth(df):
    pass

# Takes in profitability metrics (or other) df
# Returns profitability metrics df with new growth columns


def join_metrics(profitability, liquidity, solvency, cashflow, activity):
    pass
