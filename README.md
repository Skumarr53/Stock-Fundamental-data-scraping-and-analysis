# Stock-Fundamental-data-scraping-and-analysis



## Problem Statement:

Stock investing, if done properly, yield better returns over long term when compared to other conservative investment vehicles . The success comes from choosing the stocks with solid fundamentals out of thousands. However, finding these stocks is as difficult as finding unicorn. Picking a fundamentally sound stock involves investigating stocks from different angles such as evaluating fundamental ratios, company management analysis, product impact in consumer market, about its competitors, and many more. Every step is crucial in deciding the stock we want to invest in and each part demands substantial amount of time. So doing these steps on every stock is not a good idea. We have to choose only a handful of potential stocks based on certain qualifying criteria usually set on performance indicators.

This project tries to make initial stocks screening process and the most important aspect i.e reviewing trend of perfomance indicators easier. Reviewing company fundamentals involves understanding how well the company has performed over past few years by looking at annaual figures and also trend. Again, doing that manually is hectic job as it involves collecting list of list of stocks that meets our creteria, going over each stock page that is in our screened stock list, fetching historical data of performance indicators and maybe plotitng them to understand trend. So, I decided to build 'web crawler' in #python that does all this tasks at one go. Just to summarize, The objective of this project is to help users choose best value stocks that by allowing them to screen stocks based on criteria set by them and perform detailed historical performance review on the selected stocks.

## Files Description

1. Stock_FundamentalPlots.ipynb - Ipython Notebook that crawls through the list of stock pages and collects the historical data for selected performance indicatores
2. Financials_Considered.txt - List of key indicators that are used for screening potential stocks.
3. Ratios_Descriptions.txt - Short description/defination about ratio.
4. TrendPlots - Folder that contains trend plot of performance indicators for stocks.
5. Stock_Screener - csv file that has list of stocks with indicators for current financial year that can used for stock screening
6. trenddata.pkl - pickle for that stores historical perfomance data of all companies 

##




Scripts:
1. Stock_Fundamental_Data_Screener.ipynb - Financial ratios table 
Stock_FundamentalPlots.ipynb - Plots of key parameters over time 
Stock_FundamentalPlots.ipynb - Plots of key parameters over time 
