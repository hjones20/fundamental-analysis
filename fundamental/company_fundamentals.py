import pandas as pd
import os

pd.set_option('display.max_rows', None)


def prepare_data(directory, year_pattern):
    """
    Load all files in the provided directory as pandas DataFrames and join data into one large
    DataFrame for future analysis.

    :param directory: Local directory where financial data resides
    :param year_pattern: String indicating which files to pull. Example: '10Y', '5Y', '3Y', etc.
    :return: Master DataFrame containing all data from the listed directory
    :rtype: pandas.DataFrame
    """

    master = pd.DataFrame()

    for file in os.listdir(directory):

        if file.endswith(year_pattern, -7, -4):

            financial_data = pd.read_csv(directory + str(file))

            if master.empty:
                master = financial_data
            else:
                master = pd.merge(master, financial_data, on=['symbol', 'date'], how='inner')

        elif file == 'company-profiles.csv':

            company_profiles = pd.read_csv(directory + str(file))

            try:
                master = pd.merge(master, company_profiles, on='symbol', how='left')
            except KeyError:
                continue

    duplicate_cols = [x for x in master if x.endswith('_x') or x.endswith('_y')]
    master.drop(duplicate_cols, axis=1, inplace=True)

    return master


def calculate_stats(df, stat, report_year, eval_period, *args):
    """
    Calculate N year statistics for provided columns. Tickers without financials as recent as
    the specified report_year are removed.

    :param df: DataFrame containing the columns specified in *args
    :param stat: Statistic to calculate: mean, median, or percent change
    :param report_year: Ending year of calculation
    :param eval_period: Number of years to include in the calculation
    :param args: Columns that require calculations
    :return: New DataFrame containing 'symbol', 'year', and 'stat X' columns
    :rtype: pandas.DataFrame
    """

    df.sort_values(by=['symbol', 'year'], inplace=True, ascending=False)

    company_stats = pd.DataFrame()

    for arg in args:

        metric = df[['symbol', 'year', arg]]
        metric = metric.pivot_table(values=arg, index='symbol', columns='year')

        if stat == 'percent change':
            column_name = str(eval_period) + 'Y ' + arg + ' % Change'
            company_stats[column_name] = (metric.iloc[:, -1] / metric.iloc[:, 0]) - 1

        elif stat == 'mean':
            column_name = str(eval_period) + 'Y ' + arg + ' Mean'
            company_stats[column_name] = metric.mean(axis=1)

        elif stat == 'median':
            column_name = str(eval_period) + 'Y ' + arg + ' Median'
            company_stats[column_name] = metric.median(axis=1)

    company_stats['year'] = report_year

    return company_stats


def screen_stocks(df, **kwargs):
    """
    Subset DataFrame to stocks containing column values within the specified thresholds.

    :param df: DataFrame containing the columns specified in key values of **kwargs
    :param kwargs: Dictionary containing column names as keys and min/max threshold values
    :return: Subset of the DataFrame provided
    :rtype: pandas.DataFrame
    """
    df = df[['symbol', 'year', 'industry', 'Debt to Equity', 'Current ratio', 'ROE',
             'Interest Coverage']]

    for column, thresholds in kwargs.items():
        df = df[(df[column] > thresholds[0]) & (df[column] < thresholds[1]) | (df[column].isnull())]

    return df


def plot_performance(df, report_year, eval_period, *args):
    pass


def main():
    data = prepare_data('data/', '10Y')

    stats = calculate_stats(data, 'median', 2019, 2, 'Revenue', 'Net Income')

    ttm = data[data.year == 2019]
    ttm = pd.merge(ttm, stats, on=['symbol', 'year'], how='inner')

    criteria = {'Debt to Equity': [0, 0.5],
                'Current ratio': [1.5, 20.0],
                'ROE': [0.10, 0.50],
                'Interest Coverage': [15, 5000]}

    qualified_stocks = screen_stocks(ttm, **criteria)

    stock_filter = data.symbol.isin(qualified_stocks.symbol)
    data = data[stock_filter]
    data = data[['symbol', 'date', 'year']]
    print(data)


if __name__ == '__main__':
    main()
