import FundamentalAnalysis as fa

# Fetch the available companies
companies = fa.available_companies()

# Pull row names (tickers) from pandas DF returned above and cast to a list
tickers = list(companies.index)

# Initialize empty dict to store company-sector mappings
company_sector_map = {}


# Create function to perform company-sector mapping
def sector_mapping():
    for ticker in tickers[0:500]:
        company_profile = fa.profile(ticker)
        company_sector_map[ticker] = company_profile.loc['sector', 'profile']
    return company_sector_map


sector_mapping()


# Initialize empty list to store tickers of a specific sector
sector_tickers = []


# Create function to subset company_sector_map to a specific sector
def sector_selection(sector):
    for key, value in company_sector_map.items():
        if value == sector:
            sector_tickers.append(key)
    return sector_tickers


sector_selection('Technology')
print(sector_tickers)



# ticker = 'AAPL'
# print(fa.profile('AAPL'))
# print(fa.rating('AAPL'))
# print(fa.income_statement(ticker, period="annual"))
# print(fa.balance_sheet_statement(ticker, period="annual"))
# print(fa.discounted_cash_flow(ticker, period="annual"))
# print(fa.key_metrics(ticker, period="annual"))
# print(fa.financial_ratios(ticker))
# print(fa.financial_statement_growth(ticker, period="annual"))
# print(fa.profile(ticker))
