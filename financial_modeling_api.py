from urllib.request import urlopen
import json
import pandas as pd


def fetch_companies():
    '''
    :return: a pandas dataframe
    '''
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

    available_companies = pd.DataFrame(ticker_company_map, index=["symbol"]).T.sort_index()
    available_companies.to_csv('ticker_company_mapping.csv')

    return available_companies




