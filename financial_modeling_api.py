from urllib.request import urlopen
import json
import pandas as pd

# Set global printing options
pd.options.display.max_columns = 20
pd.options.display.max_rows = 100


def fetch_companies():
    """
    :return: a pandas df containing company name: stock ticker mappings, tickers without company names are excluded
    """
    response = urlopen("https://financialmodelingprep.com/api/v3/company/stock/list")
    data = response.read().decode("utf-8")
    data_json = json.loads(data)['symbolsList']

    ticker_company_map = {}

    for company in data_json:
        try:
            ticker_company_map[company['name']] = company['symbol']
        except KeyError:
            # All elements of <list> data_json have a symbol (ticker), but not necessarily a company name
            print('Company name does not exist for stock ticker: ' + str(company['symbol']))

    available_listings = pd.DataFrame(ticker_company_map, index=["symbol"]).T.sort_index()
    complete_listings = available_listings.drop('')
    complete_listings.to_csv('ticker_company_mapping.csv')

    return complete_listings


def create_profile():
    """
    :return: a pandas df containing info necessary to conduct industry/sector-specific analyses
    """
    ticker_csv = pd.read_csv('ticker_company_mapping.csv', index_col=0)

    company_data = []

    for ticker in ticker_csv['symbol']:
        response = urlopen("https://financialmodelingprep.com/api/v3/company/profile/" + ticker)
        data = response.read().decode("utf-8")
        data_json = json.loads(data)['profile']
        company_data.append(data_json)

    company_df = pd.DataFrame(company_data)
    company_df = company_df[['companyName', 'exchange', 'industry', 'website', 'description', 'ceo', 'sector']]
    company_df = company_df.set_index('companyName')

    # Merge with ticker_csv to capture ticker/symbol; join on index of both dfs: companyName
    company_profile = company_df.merge(ticker_csv, right_index=True, left_index=True, how='inner')
    company_profile.to_csv('company_profiles.csv')

    return company_profile
