from plotnine import *
import pandas as pd
import statistics
import textwrap
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


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
    Calculate N year statistics for provided columns.

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

    for column, thresholds in kwargs.items():
        df = df[(df[column] > thresholds[0]) & (df[column] < thresholds[1]) | (df[column].isnull())]

    ticker_list = list(df.symbol)

    return ticker_list


def plot_performance(df):

    df = df[['symbol', 'year', 'EPS', 'Dividend per Share', 'Book Value per Share', 'ROE',
             'Current ratio', 'Debt to Equity']]

    df = df.rename({'EPS': 'Earnings per Share', 'ROE': 'Return on Equity',
                    'Current ratio': 'Current Ratio', 'Debt to Equity': 'Debt to Equity Ratio'},
                   axis='columns')

    df['Return on Equity'] = df['Return on Equity'].apply(lambda x: x * 100.0)

    df.sort_values(by=['symbol', 'year'], inplace=True, ascending=True)
    df.dropna(inplace=True)

    label_dict = {'Earnings per Share': 'The EPS shows the company\'s profit per share. This chart '
                                        'should have a positive slope over time. Stable results '
                                        'here are extremely important for forecasting future cash '
                                        'flows. Note: if the company\'s book value has increased '
                                        'over time, the EPS should demonstrate similar growth.',

                  'Dividend per Share': 'This chart shows the dividend history of the company. '
                                        'This should have a flat to positive slope over time. If '
                                        'you see a drastic drop, it may represent a stock split '
                                        'for the company. Note: the dividend is taken from a '
                                        'portion of the EPS, the remainder goes to the book value.',

                  'Book Value per Share': 'The book value represents the liquidation value of the '
                                          'entire company (per share). It\'s important to see '
                                          'this number increasing over time. If the company pays a'
                                          ' high dividend, the book value may grow at a slower '
                                          'rate. If the company pays no dividend, the book value '
                                          'should grow with the EPS each year.',

                  'Return on Equity': 'Return on equity is very important because it show the '
                                      'return that management has received for reinvesting the '
                                      'profits of the company. If using an intrinsic value '
                                      'calculator, it\'s very important that this number is flat or'
                                      ' increasing for accurate results. Find companies with a '
                                      'consistent ROE above 8%.',

                  'Current Ratio': 'The current ratio helps measure the health of the company in '
                                   'the short term. As a rule of thumb, the current ratio should be'
                                   ' above 1.0. A safe current ratio is typically above 1.5. Look '
                                   'for stability trends within the current ratio to see how the '
                                   'company manages their short term risk.',

                  'Debt to Equity Ratio': 'The debt to equity ratio helps measure the health of '
                                          'the company in the long term. As a rule of thumb, the '
                                          'debt to equity ratio should be lower than 0.5. Look for '
                                          'stability trends within the debt/equity ratio to see how'
                                          ' the company manages their long term risk.'}

    wrapper = textwrap.TextWrapper(width=120)

    for key, value in label_dict.items():
        label_dict[key] = wrapper.fill(text=value)

    plots = []

    cols = df.columns[2:].tolist()

    for metric in cols:
        p = (ggplot(df, aes('year', metric, color='symbol'))
             + geom_line(size=1, alpha=0.8) + geom_point(size=3, alpha=0.8)
             + labs(title=metric, x='Report Year', y='', color='Ticker')
             + theme_538() + theme(legend_position='left', plot_title=element_text(weight='bold'))
             + scale_x_continuous(breaks=range(min(df['year']), max(df['year']) + 1, 1))
             + scale_y_continuous(breaks=range(min(df[metric].astype(int)),
                                               max(round(df[metric]).astype(int)) + 2, 1))
             + annotate(geom='label', x=statistics.mean((df['year'])),
                        y=max(round(df[metric]).astype(int) + 1), label=label_dict[metric],
                        size=8, label_padding=0.8, fill='#F7F7F7'))

        plots.append(p)

    return plots


def main():
    data = prepare_data('data/', '10Y')

    performance_stats = calculate_stats(data, 'median', 2019, 10, 'ROE')

    ttm = data[data.year == 2019]
    ttm = pd.merge(ttm, performance_stats, on=['symbol', 'year'], how='inner')

    criteria = {'Debt to Equity': [0, 0.5],
                'Current ratio': [1.5, 10.0],
                'ROE': [0.10, 0.50],
                '10Y ROE Median': [0.08, 0.25],
                'Interest Coverage': [15, 5000]}

    qualified_stocks = screen_stocks(ttm, **criteria)

    data = data[data['symbol'].isin(qualified_stocks)]

    visualize = plot_performance(data)


if __name__ == '__main__':
    main()
