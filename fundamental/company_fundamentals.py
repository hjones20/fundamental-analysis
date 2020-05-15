import pandas as pd

pd.options.display.max_columns = 20
pd.options.display.max_rows = 100


def calculate_growth_rates(df, report_year, eval_period, *args):
    """
    Calculate N year growth rates for provided metrics

    :param df: DataFrame containing the columns specified in *args
    :param report_year: Ending year of growth rate calculation
    :param eval_period: Number of years to include in growth rate calculation
    :param args: Columns that require growth rate calculations
    :return: New DataFrame containing 'symbol', 'year', and 'percent change' columns
    :rtype: pandas.DataFrame
    """

    df.sort_values(by=['symbol', 'year'], inplace=True, ascending=False)

    for ticker in df['symbol']:
        if df['year'][0] != report_year:
            df = df[df.symbol != ticker]

    year_filter = report_year - eval_period
    df = df[df['year'].astype(int) >= year_filter]

    company_growth_rates = pd.DataFrame()

    for arg in args:

        metric = df[['symbol', 'year', arg]]
        metric = metric.pivot_table(values=arg, index='symbol', columns='year')

        growth_rate = (metric.iloc[:, -1] / metric.iloc[:, 0]) - 1
        column_name = str(eval_period) + 'Y ' + arg + ' % Change'

        company_growth_rates[column_name] = growth_rate

    return company_growth_rates


def plot_growth_stability(df, *args):
    pass


# Change this to **kwargs: metric, value threshold
# Need min and max thresholds
def screen_metrics(df, threshold, *args):
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
    company_profiles = pd.read_csv('data/company-profiles.csv')
    company_financials = pd.read_csv('data/financials.csv')
    company_key_metrics = pd.read_csv('data/company-key-metrics.csv')

    company_profiles = company_profiles[['symbol', 'companyName', 'sector', 'industry',
                                         'website']].copy()

    company_financials = company_financials[['symbol', 'year', 'Gross Margin', 'EBIT Margin',
                                             'Net Profit Margin', 'Revenue', 'Net Income', 'EPS',
                                             'Total assets', 'Total liabilities', 'Total debt',
                                             'Free Cash Flow', 'Dividend payments']].copy()

    company_key_metrics = company_key_metrics[['symbol', 'year', 'Market Cap', 'PE ratio',
                                               'PB ratio', 'Debt to Equity', 'Current ratio',
                                               'Interest Coverage', 'ROE', 'ROIC',
                                               'Days Sales Outstanding',
                                               'Days of Inventory on Hand',
                                               'Days Payables Outstanding']].copy()

    test = calculate_growth_rates(company_financials, 2019, 10, 'Revenue', 'Net Income')
    print(test)

    # df = df[df.year == 2019]

    # subset = df[(df['Debt to Equity'] < 0.5)
    #             & (df['Current ratio'] > 1.5)
    #             & (df['ROE'] > 0.10)
    #             & (df['Interest Coverage'] > 15)]
    #
    # print(subset.shape)


if __name__ == '__main__':
    main()
