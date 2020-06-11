# Fundamental Analysis
Fundamental Analysis is a program that allows me to screen stocks using fundamental indicators and estimate the intrinsic value of qualified stocks using the Discounted Cash Flow method of valuation.

**The logic accomplishes 5 primary tasks:**

1. Downloads all stock tickers available via the FinancialModelingPrep API and generates profiles on each company
2. Retrieves and cleans financial statement data on each company
3. Screens companies on any chosen indicators of value (ex: 8-Year Median ROE)
4. Plots the stability of core indicators over an N-year period
    - Includes: EPS, Dividend Per Share, Book Value per Share, ROE, Current Ratio, Debt to Equity Ratio
5. Estimates the intrinsic value, margin of safety value for chosen companies

![alt text](https://github.com/hjones20/fundamental-analysis/blob/master/fundamental/images/EPS-scaled.png?raw=true)

## Functions
I've listed the available functions separated by module below for anyone that wishes to build upon this logic. <br/><br/>

##### Notes: 
1. The FinancialModelingPrep API appears to be updated frequently and thus data availability, functionality, or naming conventions may change.
2. It is not necessary to use the functions prefixed with the word 'calculate' in the company_fundamentals module in order to find the intrinsic value of a company. You can get a given company's discounted cash flow directly from the FinancialModeling Prep API <a href="https://financialmodelingprep.com/developer/docs/#Company-Discounted-cash-flow-value" target="_blank">here.</a> Likewise, FinancialModelingPrep offers a tutorial on Discounted Cash Flow Modeling <a href="https://financialmodelingprep.com/discounted-cash-flow" target="_blank">starting here.</a> I simply opted to build the DCF logic myself as I wanted to better understand how it worked.

- **company_profiles**
    - `get_company_data` - <a href="https://financialmodelingprep.com/developer/docs/#Symbols-List" target="_blank">Retrieves 'symbol', 'name', 'price', and 'exchange' information</a> for all available stock tickers
    - `select_stock_exchanges` - Filters out stock tickers that are not listed on one of the major exchanges: 'Nasdaq Global Select', 'NasdaqGS', 'Nasdaq', 'New York Stock Exchange', 'NYSE', 'NYSE American'
    - `select_minimum_price` - Filters out stock tickers that have a price less than the one specified by the user
    - `create_company_profile` - Retrieves <a href="https://financialmodelingprep.com/developer/docs/#Company-Profile" target="_blank">additional company information</a> for each stock ticker provided, writes data to csv file, stores file in 'data' directory
- **company_financials**
    - `select_sector` - Filters out stock tickers that do not belong to the specified sectors
    - `select_industries` - Filters out stock tickers that do not belong to the specified industries
    - `get_financial_data` - Retrieves any of the following financial statements for each of the stock tickers provided: <a href="https://financialmodelingprep.com/developer/docs/#Company-Financial-Statements" target="_blank">Financial Statements</a>, <a href="https://financialmodelingprep.com/developer/docs/#Company-Financial-Ratios" target="_blank">Financial Ratios</a>, <a href="https://financialmodelingprep.com/developer/docs/#Company-Financial-Growth" target="_blank">Financial Growth</a>, <a href="https://financialmodelingprep.com/developer/docs/#Company-Key-Metrics" target="_blank">Key Company Metrics</a>, <a href="https://financialmodelingprep.com/developer/docs/#Company-Enterprise-Value" target="_blank">Enterprise Value</a>
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
- **Data Sources:** All stock data is pulled from the <a href="https://financialmodelingprep.com/developer/docs/" target="_blank">FinancialModelingPrep API</a>
- **Graphs:** The "Stability Graph" concept was taken from the great folks at <a href="https://www.buffettsbooks.com/" target="_blank">www.buffettsbooks.com</a>. They explain why this concept is so important <a href="https://www.buffettsbooks.com/how-to-invest-in-stocks/intermediate-course/lesson-20" target="_blank">here</a>
- **Calculations:** Guides to the Discounted Cash Flow method of valuation can be found in many places across the internet. Personally, I used the <a href="https://www.udemy.com/course/advanced-value-investing" target="_blank">Advanced Value Investing Udemy course</a> 
