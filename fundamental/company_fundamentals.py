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
    pass


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


def main():
    company_financials = pd.read_csv('data/company_financials.csv')

    profitability_metrics = calculate_profitability_metrics(company_financials)
    liquidity_metrics = calculate_liquidity_metrics(company_financials)
    solvency_metrics = calculate_solvency_metrics(company_financials)
    cashflow_metrics = calculate_cashflow_metrics(company_financials)
    activity_metrics = calculate_activity_metrics(company_financials)

    joined_metrics = join_metrics(profitability_metrics, liquidity_metrics, solvency_metrics,
                                  cashflow_metrics, activity_metrics)

    growth_metrics = calculate_metric_growth(joined_metrics, 'annual')

    return growth_metrics


if __name__ == '__main__':
    main()
