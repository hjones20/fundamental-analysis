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
I've listed the available functions separated by module below for anyone that wishes to build upon this logic. <br/>

**Notes:**<br/>
1. The FinancialModelingPrep API appears to be updated frequently and thus data availability, functionality, or naming conventions may change.
2. It is not necessary to use the functions prefixed with the word **'calculate'** in the **company_fundamentals** module in order to calculate the intrinsic value of a company. You can get a given company's discounted cash flow directly from the FinancialModeling Prep API <a href="https://financialmodelingprep.com/developer/docs/#Company-Discounted-cash-flow-value" target="_blank">here.</a> Likewise, FinancialModelingPrep offers a <a href="https://financialmodelingprep.com/discounted-cash-flow" target="_blank">tutorial on the discounted cash flow methodology here.</a> I simply opted to build the DCF logic myself in order to better understand how it works. It was not a great programming choice as errors will result if column names change.

- **company_profiles**
    - `get_company_data` - <a href="https://financialmodelingprep.com/developer/docs/#Symbols-List" target="_blank">Retrieves 'symbol', 'name', 'price', and 'exchange' information</a> for all available stock tickers
    - `select_stock_exchanges` - Filters out stock tickers that are not listed on one of the major exchanges: 'Nasdaq Global Select', 'NasdaqGS', 'Nasdaq', 'New York Stock Exchange', 'NYSE', 'NYSE American'
    - `select_minimum_price` - Filters out stock tickers that have a price less than the one specified by the user
    - `create_company_profile` - Retrieves <a href="https://financialmodelingprep.com/developer/docs/#Company-Profile" target="_blank">additional company information</a> for each stock ticker provided, writes data to csv file, stores file in the specified directory
- **company_financials**
    - `select_sector` - Filters out stock tickers that do not belong to the specified sectors
    - `select_industries` - Filters out stock tickers that do not belong to the specified industries
    - `get_financial_data` - Retrieves any of the following financial datasets for each of the stock tickers provided: <a href="https://financialmodelingprep.com/developer/docs/#Company-Financial-Statements" target="_blank">Financial Statements</a>, <a href="https://financialmodelingprep.com/developer/docs/#Company-Financial-Ratios" target="_blank">Financial Ratios</a>, <a href="https://financialmodelingprep.com/developer/docs/#Company-Financial-Growth" target="_blank">Financial Growth</a>, <a href="https://financialmodelingprep.com/developer/docs/#Company-Key-Metrics" target="_blank">Key Company Metrics</a>, <a href="https://financialmodelingprep.com/developer/docs/#Company-Enterprise-Value" target="_blank">Enterprise Value</a>
    - `clean_financial_data` - Scans DataFrame containing financial data on N stock stickers and removes rows with corrupted date values. Adds a new 'year' column as well for future use
    - `select_analysis_years` - Remove stock tickers without financial reports in a specified timeframe (ex: L10Y) and subset DataFrame to only include the years specified (ex: 2015 - 2020)
- **company_fundamentals**
    - `combine_data` - Read and join all files in a specified directory (ex: 'data/') with a specified year pattern (ex: '2Y')
    - `calculate_stats` - Calculate the mean, median, or percent change of provided columns over an N-year period
    - `screen_stocks` - Filter out stock tickers with column values that do not fall within specified ranges
    - `plot_performance` - Plot stock performance over time with respect to the following column values: 'Earnings per Share', 'Dividend per Share', 'Book Value per Share', 'Return on Equity', 'Current Ratio', 'Debt to Equity Ratio'. Note that 'Dividend per Share' is commented out as the column name seems to have disappeared in a recent API update
    - `prepare_valuation_inputs` - Subset DataFrame to include only the data required for Discounted Cash Flow model calculations
    - `calculate_discount_rate` - Calculated the Weighted Average Cost of Capital (WACC) for each stock ticker provided
    - `calculate_discounted_free_cash_flow` - Calculate the present value of discounted future cash flows for each stock ticker provided
    - `calculate_terminal_value` - Calculate the terminal value for each stock ticker for each stock ticker provided
    - `calculate_intrinsic_value` - Calculate the intrinsic value of each stock ticker provided
    - `calculate_margin_of_safety` - Calculate the margin of safety value of each stock ticker provided 


## References
- **Data Sources:** All stock data is pulled from the <a href="https://financialmodelingprep.com/developer/docs/" target="_blank">FinancialModelingPrep API</a>
- **Graphs:** The "Stability Graph" concept was taken from the great folks at <a href="https://www.buffettsbooks.com/" target="_blank">www.buffettsbooks.com</a>. They explain why this concept is so important <a href="https://www.buffettsbooks.com/how-to-invest-in-stocks/intermediate-course/lesson-20" target="_blank">here</a>
- **Calculations:** Guides to the Discounted Cash Flow method of valuation can be found in many places across the internet. Personally, I used the <a href="https://www.udemy.com/course/advanced-value-investing" target="_blank">Advanced Value Investing Udemy course</a> 
