# Web Crawler for scraping Financial data  



## Problem Statement:

Stock investing, if done properly, yield better returns over long term when compared to other conservative investment vehicles . The success comes from choosing the stocks with solid fundamentals out of thousands. However, finding these stocks is as difficult as finding unicorn. Picking a fundamentally sound stock involves investigating stocks from different angles such as evaluating fundamental ratios, company management analysis, product impact in consumer market, about its competitors, and many more. Every step is crucial in deciding the stock we want to invest in and each part demands substantial amount of time. So doing these steps on every stock is not a good idea. We have to choose only a handful of potential stocks based on certain criteria usually set on performance indicators. But reviewing fundamentals of current does not reveal much information and sometimes may also be misleading because for some reason situation may be different in that financial year. Instead we need take to look at performance indicators for past few years to get clear picture about the comany's perfomance.

This project tries to make initial stocks screening process and the most important aspect i.e reviewing trend of perfomance indicators easier. Reviewing company fundamentals involves understanding how well the company has performed over past few years by looking at annaual figures and also trend. Again, doing that manually is hectic job as it involves collecting list of list of stocks that meets our creteria, going over each stock page that is in our screened stock list, fetching historical data of performance indicators and maybe plotitng them to understand trend. So, I decided to build 'web crawler' in #python that does all this tasks at one go. Just to summarize, The objective of this project is to help users choose best value stocks that by allowing them to screen stocks based on criteria set by them and perform detailed historical performance review on the selected stocks.

## Files Description

1. Stock_FundamentalPlots.ipynb - Ipython Notebook that crawls through the list of stock pages and collects the historical data for selected performance indicators
2. Financials_Considered.txt - List of key indicators that are used for screening potential stocks.
3. Ratios_Descriptions.txt - Short description/defination about indicators.
4. TrendPlots - Folder that contains trend plot of indicators historical performance of stocks.
5. Stock_Screener - csv file that has list of stocks with indicators for current financial year that can used for stock screening
6. trenddata.pkl - pickle for that stores historical perfomance data of all companies

## Approch:

 This approch involves following steps:
 1. Logging into a data provider server.
 2. Submitting the query that filters the stocks qualifying our criteria
 3. Collecting the stocks links storing in list from the first page (if results are more than a page).
 4. Looping over stock link page and fetching required data, and simultaneously generating Plots for every link.
 5. Move to next page and repeat step 3-4 until it hits last page.

Requirements:
1. Python: the Web craweler is built in Python
2. Selenium: tool that interacts with web server on backend
3. Beautifulsoap: package that helps to fetch data form HTML docment
4. Numpy: Raw data which is text format is converted and stored in numeric array fromat
5. Matplotlib: Plots Generation


1. In this step we intialize the selenium webdriver and use that to log in into the web sever by submitting our credentials. Screener.in is the data source and Login link is provided below. https://www.screener.in/login/

![Loign page](ScreenShots/LoginPage.png)

2. Once we successfully get inside server now we have access to the data. now we can run our query to to filter the stock that pass our desired criteria. I have set simple query that 'market capitalization > 0'. After running this query it lists out all the companies that have market capitaization above zero. Below is the screenshot of resulting page.

query link: https://www.screener.in/screen/raw/?sort=&source=&order=&page=1&query=Market+Capitalization%3E0

![Query page](ScreenShots/QueryPage.png)

Notice that there are 3879 results that passes the creteria set by us and they are stored across 156 pages. we need to insert the page number in the query link embeded at "&page=1&" to crawl across the pages 1-156 to get all the resulted stock links. For Now, we are in page 1, lets collect all the stock page links and store them in list. the links can be scraped by extracting 'href' tags associated with stock links using 'bs4' package. We need to visit each stock page to source the data from it. It's done by creating beautifulsoup object of page, then locating tags that corresponds to the data we are interested in and storing the data in array format. below scroll over the example to get glance of web page.

![page visual scan](ScreenShots/page_scan.gif)


The page contains several tables of historial data of parameters that describes the past perfomance and financial health of the company. But I have considered only few indicators based on my intiuation that decides stabilty and profitability of a company inthe competative environment in the long run. You will see the selected indicators on the plot generated in a while.

Collecting just numbers won't tell much as it is difficult interpect just looking at number. we can create visual plots on the fly that tells the story about the company and may give hints on where it is heading in future. Below I have added trend plot of performance indicators for Avanti Feeds Ltd comany as an example case. Company is mainly into aquacultural feed manufacturing business along production of value added products of shrimps.

![Trend of Fundamental ratio](ScreenShots/Miscellaneous_Avanti_Feeds_Ltd.png)

I will present here some of my insights about its management. Lets go over them.

1. Sales growth - company has aggresviely expanded its sales (>50%) but its droped in recent years suggest that company is close to attain market saturation. But still It has maintained above 25 % most of financial years.
2. Operating profit Margin - company overall operating margin shows positive trend. It signifies that difference between sales revenue and product manufacturing growing. Notice that there is shrap rise in 2017 can be attributed to drop in raw materials price. Also drop in current years can be attributed rise in raw materials price above normal range upon doing some research.
3. Net profit growth growth - This has same story as the above. The company Net profit margin in recent years is close to 8-9% which is decent number. Company profit showing positive trend is a good sign.
4. Asset Purchased - Asset purchase can be associated with bussiness expansion or improvemwnt such replacing existing, entering into new market segmeant or new business. Significant positve value indicates company is growing.
5. Reinvestment into Business - Reinvestment into Business is almost same as previous one but expressed in percentage of sales revenue. This will give better picture about company's growth. Suppose, there are two companies A and B of market capitaization 100 cr and 1000 cr. Both companies Reinvesting 10 cr into business is not same. A is expanding in business by 10% whereas B is expanding by only 1%. A is more aggresive when compared to B. The Avanti Feeds has maintained above 10% most of the years which is good number for a company of this size.
6. Return on Capital employed - Idea is generally capital invested should yield higher percent returns or else company is not making best use of its resouces. Its lose indicator need not be taken seriously because capital invested this year may not get converted into returns same year but in long run is yield good returns. So investors should focus long term trend rather than just numbers.
7. Free cash flows - It is the cash left with the company after decucting tax paid, capital expenditure and net working capital from earnings. This is the actual cash availble to owners, shareholders and lenders. Hence, This number more meangingful than net profit in terms business returns and it forms the base input for stock price evaluation. For Avanti Feeds has shows incresing trend however actual number also matters.
8. Debt - Debt is one of the factor that decides stability of the company if not keep under control may lead to downfall of the company in weak economy. Increasing trend tells that company is strugglig to meet its financial needs. This company is almost free from debt which is good.
9. EPS - Earnings per share is the profit earned by shareholder per share. From 2011 onwards the EPS value is monotonically increasing till 2018 which means the investors has positive sentiment towards the company and confident about the company's growth in future. Seems likes drop in the Sale growth and profit margins in 2019 financial year may have negatively impacted EPS.  

These insights just scractes the surface there is more to it like understanding interactions between indicators give even better insights. Reading plots and developing story is an art that can be mastered by practice and experience. It is advised go over past few year financial reports to know the actual reasons behind changes obsevered in plots.

Now we scraped data for first company on the first page. this excercise has to be repeated for all the stocks in the first page, then move to second page and so on iteratively.   









Scripts:
1. Stock_Fundamental_Data_Screener.ipynb - Financial ratios table
Stock_FundamentalPlots.ipynb - Plots of key parameters over time
Stock_FundamentalPlots.ipynb - Plots of key parameters over time
