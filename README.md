# Fundamental Analysis
Fundamental Analysis is a program that allows me to screen stocks using fundamental indicators and estimate the intrinsic value of qualified stocks using a Discounted Cash Flow method of valuation.

**The logic accomplishes 5 primary tasks:**

1. Downloads all stock tickers available via the FinancialModelingPrep API and generates profiles on each company
2. Retrieves and cleans financial statement data on each company
3. Screens companies on any chosen indicators of value (ex: 5-Year Median ROE)
4. Plots the stability of core indicators over an N-year period
    - Includes: EPS, Dividend Per Share, Book Value per Share, ROE, Current Ratio, Debt to Equity Ratio
5. Estimates the intrinsic value, adjusted margin of safety value for chosen companies

![alt text](https://github.com/hjones20/fundamental-analysis/blob/master/fundamental/images/EPS-scaled.png?raw=true)

# References
- All stock data is pulled from the FinancialModelingPrep API: https://financialmodelingprep.com/developer/docs/ <br/><br/>
- The "Stability Graph" concept was taken from the great folks at https://www.buffettsbooks.com. You can find their explanation of the concept here: https://www.buffettsbooks.com/how-to-invest-in-stocks/intermediate-course/lesson-20 <br/> <br/>
- References for the Discounted Cash Flow methodology of valuation can be found in many places across the internet. Personally, I used the following Udemy course: https://www.udemy.com/course/advanced-value-investing 
