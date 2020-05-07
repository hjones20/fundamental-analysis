import pandas as pd

pd.options.display.max_columns = 20
pd.options.display.max_rows = 100


def profitability_metrics(df):
    """
    Calculate profitability metrics for N companies.

    :param df: DataFrame containing financial statement data on N companies
    :return: DataFrame containing profitability metrics for N companies
    :rtype: pandas.DataFrame
    """
    metrics = df[['symbol', 'date']].copy()

    metrics['Gross Profit Margin'] = df['Gross Profit'] / df['Revenue']
    metrics['EBITDA Margin'] = df['EBITDA'] / df['Revenue']
    metrics['Operating Profit Margin'] = df['Operating Income'] / df['Revenue']
    metrics['Net Profit Margin'] = df['Net Income'] / df['Revenue']

    metrics['COGS to Sales'] = df['Cost of Revenue'] / df['Revenue']

    metrics['SG&A to Sales'] = df['SG&A Expense'] / df['Revenue']
    metrics['R&D to Sales'] = df['R&D Expenses'] / df['Revenue']
    metrics['Operating Expense to Sales'] = df['Operating Expenses'] / df['Revenue']

    metrics['Interest Expense to Sales'] = df['Interest Expense'] / df['Revenue']
    metrics['Income Tax to Sales'] = df['Income Tax Expense'] / df['Revenue']

    # metrics['Return on Equity'] = df['Net Income'] / df['Total assets'] - df['Total liabilities']
    # metrics['Return on Assets'] = df['Net Income'] / df['Total assets']
    # Return on Invested Capital (key metrics)
    #
    # metrics['Book Value'] = df['Total assets'] - df['Total liabilities']
    # metrics['Owners Earnings or FCF'] = df['Operating Cash Flow'] - df['Capital Expenditure']
    # metrics['FCF Margin'] = (df['Operating Cash Flow'] - df['Capital Expenditure']) /df['Revenue']
    #
    # metrics['Cash Flow to CAPEX Ratio'] = df['Operating Cash Flow'] / df['Capital Expenditure']

    return metrics


def liquidity_metrics(df):
    """
    Calculate liquidity metrics for N companies.

    :param df: DataFrame containing financial statement data on N companies
    :return: DataFrame containing liquidity metrics for N companies
    :rtype: pandas.DataFrame
    """
    metrics = df[['symbol', 'date']].copy()

    metrics['Current Ratio'] = df['Total current assets'] / df['Total current liabilities']
    metrics['Quick Ratio'] = (df['Cash and cash equivalents'] + df['Short-term investments']
                              + df['Receivables']) / df['Total current liabilities']
    metrics['Cash Ratio'] = df['Cash and cash equivalents'] / df['Total current liabilities']

    # DSO = Days Sales Outstanding (key metrics)
    # DIO = Days Inventory Outstanding (key metrics - "Days of Inventory on Hand")
    # DPO = Days Payables Outstanding (key metrics)

    # Operating Cycle = DSO + DIO (calculate from metrics above)
    # Cash Conversion Cycle = DSO + DIO - DPO (calculate from metrics above)

    return metrics


def solvency_metrics(df):
    """
    Calculate solvency metrics for N companies.

    :param df: DataFrame containing financial statement data on N companies
    :return: DataFrame containing solvency metrics for N companies
    :rtype: pandas.DataFrame
    """
    metrics = df[['symbol', 'date']].copy()

    metrics['Debt Ratio'] = df['Total liabilities'] / df['Total assets']
    metrics['Debt to Equity Ratio'] = df['Total Debt'] / df['Total shareholders equity']
    metrics['Interest Coverage Ratio'] = df['EBIT'] / df['Interest Expense']
    metrics['Cash Flow to Debt Ratio'] = df['Operating Cash Flow'] / df['Total Debt']
    metrics['Working Capital to Debt Ratio'] = \
        (df['Total current assets'] - df['Total current liabilities']) / (df['Short-term debt'] +
                                                                          df['Long-term debt'])


def cashflow_metrics(df):
    """
    Calculate cash-flow metrics for N companies.

    :param df: DataFrame containing financial statement data on N companies
    :return: DataFrame containing cash-flow metrics for N companies
    :rtype: pandas.DataFrame
     """
    metrics = df[['symbol', 'date', 'Operating Cash Flow']].copy()

    metrics['Operating Cash Flow Margin'] = df['Operating Cash Flow'] / df['Revenue']
    metrics['Free Cash Flow'] = df['Operating Cash Flow'] - df['Capital Expenditure']

    return metrics


def activity_metrics(df):
    """
    Calculate activity metrics for N companies.

    :param df: DataFrame containing financial statement data on N companies
    :return: DataFrame containing activity metrics for N companies
    :rtype: pandas.DataFrame
    """
    # Cash to Current Assets
    # Inventory to Current Assets
    # Accounts Receivable to Current Assets
    # Accounts Payable to Current Assets

    # SG&A as % of gross profit (less than 30% is great - consistency indicates DCA)
    # Depreciation as % of gross profit


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


def metric_growth(df, period):
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

    company_profitability = profitability_metrics(company_financials)
    # company_liquidity = liquidity_metrics(company_financials)
    # company_solvency = solvency_metrics(company_financials)
    # company_cashflow = cashflow_metrics(company_financials)
    # company_activity = activity_metrics(company_financials)
    #
    # joined_metrics = join_metrics(company_profitability,
    #                               company_liquidity,
    #                               company_solvency,
    #                               company_cashflow,
    #                               company_activity)
    #
    # growth_metrics = metric_growth(joined_metrics, 'annual')
    #
    # return growth_metrics
    print(company_financials.columns)
    print(company_profitability.head(20))


if __name__ == '__main__':
    main()
