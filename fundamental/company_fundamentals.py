import pandas as pd

pd.options.display.max_columns = 20
pd.options.display.max_rows = 100

dat = pd.read_csv('data/company-key-metrics.csv')


def get_trailing_twelve_months(df):
    """
    Subset DataFrame to trailing twelve months of data.

    :param df: DataFrame containing stock tickers (symbol) and dates for N companies
    :return: Subset of the DataFrame provided
    :rtype: pandas.DataFrame
    """
    df.sort_values(by=['symbol', 'date'], inplace=True, ascending=False)
    df = df.groupby('symbol').nth(0)

    return df


def filter_metrics(df, threshold, *args):
    """
    Subset DataFrame to stocks with column values above the specified threshold.

    :param df: DataFrame containing the column names specified in *args
    :param threshold: Number that each column value should exceed
    :param args: Column values to subset
    :return: Subset of the DataFrame provided
    :rtype: pandas.DataFrame
    """
    for arg in args:
        df = df[df[arg] > threshold]

    return df


def get_growth_rates(df, report_year, eval_period, *args):

    df.sort_values(by=['symbol', 'date'], inplace=True, ascending=False)
    df['year'] = df['date'].str[:4]

    year_filter = report_year - eval_period
    df = df[df['year'].astype(int) >= year_filter]

    for arg in args:
        metric = df[['symbol', 'year', arg]]
        metric.index = metric['year']
        print(metric.transpose())
        # Create pivot table instead
        # Year = cols
        # Symbol = rows
        # Metric = values


def get_growth_stability(df, *args):
    pass


# For loop: read everything in as DataFrame with variable name matching filename
ttm_dat = get_trailing_twelve_months(dat)
filtered_dat = filter_metrics(ttm_dat, 0, 'ROE', 'Interest Coverage', 'Free Cash Flow per Share')
print(get_growth_rates(dat, 2019, 5, 'ROE', 'Interest Coverage', 'Free Cash Flow per Share'))
