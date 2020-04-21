import FundamentalAnalysis as fa
import pandas as pd
import matplotlib.pyplot as plt

# Set global printing options
pd.options.display.max_columns = 20
pd.options.display.max_rows = 100

# Fetch the available company profiles
company_profiles = pd.read_csv('company_profiles.csv')

# Select your circle of competence
sector_company_counts = company_profiles['sector'].value_counts(dropna=False)
industry_company_counts = company_profiles['industry'].value_counts(dropna=False)


def select_sector(df, sector):
    sector_filter = df['sector'] == sector
    sector_profiles = df[sector_filter]
    return sector_profiles


def select_industry(df, industry):
    industry_filter = df['industry'] == industry
    industry_profiles = df[industry_filter]
    return industry_profiles




