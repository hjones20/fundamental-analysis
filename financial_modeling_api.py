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

fetch_companies()


#
# #ticker_csv = pd.read_csv('ticker_company_mapping.csv', index_col=0)
# print(ticker_csv)
#
# company_data = []
#
# for ticker in ticker_csv['symbol'][0:3]:
#     response = urlopen("https://financialmodelingprep.com/api/v3/company/profile/" + ticker)
#     data = response.read().decode("utf-8")
#     data_json = json.loads(data)['profile']
#     company_data.append(data_json)
#
# company_df = pd.DataFrame(company_data)
# company_df = company_df[['companyName', 'exchange', 'industry', 'website', 'description', 'ceo', 'sector']]
#
# # Remove rows with missing values
# company_df = company_df.loc[company_df['companyName'] != '']
#
# # Merge with ticker_csv to capture ticker; join on companyName
#
#
# # print(company_profile)
# # print(len(company_profile))