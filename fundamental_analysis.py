import FundamentalAnalysis as fa


# Show the available companies
companies = fa.available_companies()

# Pull row names (tickers) from pandas DF above and cast to a list
tickers = list(companies.index)

# initialize empty sector list
sector_companies = []

# TODO: Add a decorator function to show how long this function takes to return a result when called
# subset companies by sector
def select_sector(sector):
    for ticker in tickers[0:200]:
        company_profile = fa.profile(ticker)
        if company_profile.loc['sector', 'profile'] == sector:
            sector_companies.append(ticker)
    return sector_companies

sector_tickers = select_sector('Technology')
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

