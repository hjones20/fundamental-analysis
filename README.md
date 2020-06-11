# Fundamental Analysis
Fundamental Analysis is a program that allows me to screen stocks using fundamental indicators and estimate the intrinsic value of qualified stocks using a Discounted Cash Flow method of valuation.

**The logic accomplishes 5 primary tasks:**

1. Downloads all stock tickers available via the FinancialModelingPrep API and generates profiles on each company
2. Retrieves and cleans financial statement data on each company
3. Screens companies on any chosen indicators of value (ex: 8-Year Median ROE)
4. Plots the stability of core indicators over an N-year period
    - Includes: EPS, Dividend Per Share, Book Value per Share, ROE, Current Ratio, Debt to Equity Ratio
5. Estimates the intrinsic value, margin of safety value for chosen companies

![alt text](https://github.com/hjones20/fundamental-analysis/blob/master/fundamental/images/EPS-scaled.png?raw=true)

## Functions
I've listed the available functions separated by module below for anyone that wishes to build on this logic. Note that the FinancialModelingPrep API appears to be updated frequently and thus, data availability, functionality, or naming conventions may change. <br/>
- **company_profiles**
    - `get_company_data` - xxx
    - `select_stock_exchanges` - xxx
    - `select_minimum_price` - xxx
    - `create_company_profile` - xxx
- **company_financials**
    - `select_sector` - xxx
    - `select_industries` - xxx
    - `get_financial_data` - xxx
    - `clean_financial_data` - xxx
    - `select_analysis_years` - xxx
- **company_fundamentals**
    - `combine_data` - xxx
    - `calculate_stats` - xxx
    - `screen_stocks` - xxx
    - `plot_performance` - xxx
    - `prepare_valuation_inputs` - xxx
    - `calculate_discount_rate` - xxx
    - `calculate_discounted_free_cash_flow` - xxx
    - `calculate_terminal_value` - xxx
    - `calculate_intrinsic_value` - xxx
    - `calculate_margin_of_safety` - xxx


## References
- **Data Sources:** All stock data is pulled from the FinancialModelingPrep API: https://financialmodelingprep.com/developer/docs/ <br/><br/>
- **Graphs:** The "Stability Graph" concept was taken from the great folks at https://www.buffettsbooks.com. You can find their explanation of the concept here: https://www.buffettsbooks.com/how-to-invest-in-stocks/intermediate-course/lesson-20 <br/> <br/>
- **Calculations:** Guides to the Discounted Cash Flow method of valuation can be found in many places across the internet. Personally, I used the following Udemy course: https://www.udemy.com/course/advanced-value-investing 
