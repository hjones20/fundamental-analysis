import pandas as pd

pd.options.display.max_columns = 20
pd.options.display.max_rows = 100


def calculate_profitability_metrics(df):
    """
    Calculate profitability metrics for N companies.

    :param df: DataFrame containing financial statement data on N companies
    :return: DataFrame containing profitability metrics for N companies
    :rtype: pandas.DataFrame
    """

    # EBIT Margin = Operating Profit Margin
    data = df[['symbol', 'date', 'Gross Margin', 'EBIT Margin', 'Net Profit Margin',
               'Operating Cash Flow']].copy()

    data['Return on Equity'] = df['Net Income'] / df['Total shareholders equity']
    data['Return on Assets'] = df['Net Income'] / df['Total assets']

    data['Working Capital'] = df['Total current assets'] - df['Total current liabilities']

    data['Cash to Current Assets'] = df['Cash and cash equivalents'] / df['Total current assets']
    data['Inventory to Current Assets'] = df['Inventories'] / df['Total current assets']
    data['Receivables to Current Assets'] = df['Receivables'] / df['Total current assets']
    data['Payables to Current Assets'] = df['Payables'] / df['Total current assets']

    data['Current Ratio'] = df['Total current assets'] / df['Total current liabilities']
    data['Interest Coverage Ratio'] = df['EBIT'] / df['Interest Expense']
    data['Working Capital to Debt'] = (df['Total current assets']
                                       - df['Total current liabilities']) / \
                                      (df['Short-term debt'] + df['Long-term debt'])

    data['Free Cash Flow'] = data['Operating Cash Flow'] - df['Capital Expenditure']

    data['Dividend Payout Ratio'] = df['Dividend per Share'] / df['EPS']

    return data


def calculate_liquidity_metrics(df):
    """
    Calculate liquidity metrics for N companies.

    :param df: DataFrame containing financial statement data on N companies
    :return: DataFrame containing liquidity metrics for N companies
    :rtype: pandas.DataFrame
    """

    pass


def calculate_solvency_metrics(df):
    """
    Calculate solvency metrics for N companies.

    :param df: DataFrame containing financial statement data on N companies
    :return: DataFrame containing solvency metrics for N companies
    :rtype: pandas.DataFrame
    """
    pass


def calculate_cashflow_metrics(df):
    """
    Calculate cash-flow metrics for N companies.

    :param df: DataFrame containing financial statement data on N companies
    :return: DataFrame containing cash-flow metrics for N companies
    :rtype: pandas.DataFrame
     """
    pass


def calculate_activity_metrics(df):
    """
    Calculate activity metrics for N companies.

    :param df: DataFrame containing financial statement data on N companies
    :return: DataFrame containing activity metrics for N companies
    :rtype: pandas.DataFrame
    """
    pass


def join_metrics(profitability, liquidity, solvency, cashflow, activity):
    """
    Join metric data for all stock tickers provided.

    :param profitability: DataFrame containing profitability data on N companies
    :param liquidity: DataFrame containing liquidity data on N companies
    :param solvency: DataFrame containing solvency data on N companies
    :param cashflow: DataFrame containing cashflow data on N companies
    :param activity: DataFrame containing activity data on N companies
    :return: DataFrame with the five provided metric DataFrames inner joined
    :rtype: pandas.DataFrame
    """
    pass


def calculate_metric_growth(df, period):
    """
    Calculate period growth rates of core metrics, write to csv.

    :param df: DataFrame containing previously calculated profitability, liquidity, etc. metrics
    :param period: String 'annual' or 'quarter'
    :return: DataFrame provided, plus additional growth-rate columns
    :rtype: pandas.DataFrame
    """
    pass
    # subset to list of columns we need to calculate growth for...
    # FOR EACH COLUMN SELECTED: pivot and calculate ttm and 1, 3, 5 year growth rates and then
    # unpivot / transpose

# ======================================
# ADD COMMON SIZE ANALYSIS FUNCTION
# ======================================


def main():
    company_financials = pd.read_csv('data/company_financials.csv')

    profitability_metrics = calculate_profitability_metrics(company_financials)
    # liquidity_metrics = calculate_liquidity_metrics(company_financials)
    # solvency_metrics = calculate_solvency_metrics(company_financials)
    # cashflow_metrics = calculate_cashflow_metrics(company_financials)
    # activity_metrics = calculate_activity_metrics(company_financials)
    #
    # joined_metrics = join_metrics(profitability_metrics, liquidity_metrics, solvency_metrics,
    #                               cashflow_metrics, activity_metrics)
    #
    # growth_metrics = calculate_metric_growth(joined_metrics, 'annual')
    #
    # return growth_metrics
    print(company_financials.columns)
    print(profitability_metrics.head())


if __name__ == '__main__':
    main()
