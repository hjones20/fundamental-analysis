import FundamentalAnalysis as fa
import pandas as pd

# Set global printing options
pd.options.display.max_columns = 20
pd.options.display.max_rows = 100

# Fetch the available company profiles
company_profiles = pd.read_csv('company_profiles.csv')

# ---------------------------------
# Select your circle of competence
# ---------------------------------
sector_company_counts = company_profiles['sector'].value_counts(dropna=False)
industry_company_counts = company_profiles['industry'].value_counts(dropna=False)


def select_sector(df, sector):
    sector_filter = df['sector'] == sector
    sector_profiles = df[sector_filter]
    print('Found ' + str(len(sector_profiles)) + ' companies in the ' + sector + ' sector!')
    return sector_profiles


tech_companies = select_sector(company_profiles, 'Technology')


def select_industry(df, industry):
    industry_filter = df['industry'] == industry
    industry_profiles = df[industry_filter]
    print('Found ' + str(len(industry_profiles)) + ' companies in the ' + industry + ' industry!')
    return industry_profiles


# ---------------------------------
# Filter #1: Profitability Ratios
# ---------------------------------
# Filter out companies with negative GPM, OPM, or NPM in 2019

# Create function to fetch profitability ratios directly from API

# Create function to filter based on profitability ratios
def profitability_filter(df):
    print('Looking for positive GPM, OPM, and NPM ratios among ' + str(len(tech_companies)) + ' companies...')
    positive_ratio_companies = []
    for ticker in df['symbol']:
        results = fa.financial_ratios(ticker)
        subset_year = results.iloc[:,0]
        subset_ratios = subset_year.loc[['grossProfitMargin', 'operatingProfitMargin', 'netProfitMargin']]
        for ratio in subset_ratios:
            if float(ratio) < 0.0:
                continue
            else:
                positive_ratio_companies.append(ticker)
    print('Found ' + str(len(positive_ratio_companies)) + ' companies with positive profitability ratios')
    return positive_ratio_companies


profitability_filter(tech_companies)

# ---------------------------------
# Filter #2: Earnings Manipulation
# ---------------------------------

