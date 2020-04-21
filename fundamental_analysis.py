import FundamentalAnalysis as fa
import pandas as pd

# Set global printing options
pd.options.display.max_columns = 20
pd.options.display.max_rows = 100

# Fetch the available company profiles
company_profiles = pd.read_csv('company_profiles.csv')
print(company_profiles.head())


def select_industry(industry):
    industry_filter = company_profiles['industry'] == industry
    industry_profiles = company_profiles[industry_filter]
    return industry_profiles


def select_sector(sector):
    sector_filter = company_profiles['sector'] == sector
    sector_profiles = company_profiles[sector_filter]
    return sector_profiles



