import pandas as pd

pd.options.display.max_columns = 20
pd.options.display.max_rows = 100

dat = pd.read_csv('data/company-key-metrics.csv')


def calculate_growth_rates(df, report_year, eval_period, *args):
    """
    Calculate N year growth rates for provided metrics

    :param df: DataFrame containing the columns specified in *args
    :param report_year: Ending year of growth rate calculation
    :param eval_period: Number of years to include in growth rate calculation
    :param args: Columns that require growth rate calculations
    :return:
    """

    df.sort_values(by=['symbol', 'date'], inplace=True, ascending=False)
    df['year'] = df['date'].str[:4]

    year_filter = report_year - eval_period
    df = df[df['year'].astype(int) >= year_filter]

    company_growth_rates = pd.DataFrame()

    for arg in args:

        metric = df[['symbol', 'year', arg]]
        metric = metric.pivot_table(values=arg, index='symbol', columns='year')

        growth_rate = (metric.iloc[:, -1] / metric.iloc[:, 0]) - 1
        column_name = str(eval_period) + 'Y ' + arg

        company_growth_rates[column_name] = growth_rate

    return company_growth_rates


def get_growth_stability(df, *args):
    pass


# Change this to **kwargs: metric, value threshold
def filter_metrics(df, threshold, *args):
    """
    Subset DataFrame to stocks with column values above the specified threshold.

    :param df: DataFrame containing the columns specified in *args
    :param threshold: Number that each column value should exceed
    :param args: Column values to subset
    :return: Subset of the DataFrame provided
    :rtype: pandas.DataFrame
    """
    for arg in args:
        df = df[df[arg] > threshold]

    return df


def main():
    pass
