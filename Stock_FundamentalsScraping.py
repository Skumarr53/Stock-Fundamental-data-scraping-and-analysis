# plotting Trends
import re
import numpy as np
from numpy import inf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import seaborn as sns
sns.set() # setting seaborn default for plots
from pdb import set_trace

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
dr = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)

dr.get("https://www.screener.in/login/")

username = dr.find_element_by_id("id_username")
username.clear()
username.send_keys("skumarr53@gmail.com")

password = dr.find_element_by_id("id_password")
password.clear()
password.send_keys("Skumarr53@")

dr.find_element_by_css_selector('body > main > div > div > div:nth-child(2) > form > button').click()
i=1


matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)

def css2np(css,years):
    ls = []
    for i in range(2,len(years)+2):
        ls.append(dr.find_element_by_css_selector(css+' > td:nth-child('+str(i)+')').text.replace('%','').replace(',',''))
    return pd.to_numeric(np.array(ls), errors='coerce')


#### for loop

dr.get(
    'https://www.screener.in/screen/raw/?sort=&order=&source=&query=Market+Capitalization%3E0'
)   # filtered or screened link from screener 
lastpage = int(
    dr.find_element_by_css_selector(
        'body > main > div > div.card.card-large > div.flex-row.flex-gap-8.flex-space-between.flex-align-center > div.sub').text.split(' ')[-1])

for i in list(range(1,4)):  #lastpage+1
    print(i)
    url = f'https://www.screener.in/screen/raw/?sort=&source=&page={i}&query=Market+Capitalization>0'
    dr.get(url)
    time.sleep(1)
    html = dr.page_source
    soup = bs(html)
    pageLinks = list(
        map(lambda x: x.get('href'),
            soup.findAll('a', attrs={'href': re.compile("/company/")}))) 
    
    for j in pageLinks[:3]: #[pageLinks.index(j):]
        # Stock url
        #j=pageLinks[1]
        stockUrl = 'https://www.screener.in' + j
        dr.get(stockUrl)
        time.sleep(2)
        scrnid = dr.find_element_by_css_selector('#company-info').get_attribute('data-company-id')
        
        years = np.asarray([
                    x for x in dr.find_element_by_css_selector(
                        '#profit-loss > div.responsive-holder > table > thead').text.
                    split(' ') if '20' in x
                ]).astype(int)
        
        Sector = dr.find_element_by_css_selector('#peers > div.flex.flex-space-between > div:nth-child(1) > p > a:nth-child(1)').text.replace('\n', "")
        
        ####-------------Fundamentals
        # SalesGrowth ratio
        salesCss = '#profit-loss > div.responsive-holder > table > tbody > tr:nth-child(1)'
        sales = css2np(salesCss,years)
        dr.find_element_by_xpath('//*[@id="profit-loss"]/div[2]/table/tbody/tr[1]/td[1]/button').click()        
        
        SalesGcss = '#profit-loss > div.responsive-holder > table > tbody > tr:nth-child(2)'
        SalesG = css2np(SalesGcss,years)
        dr.find_element_by_xpath('//*[@id="profit-loss"]/div[2]/table/tbody/tr[1]/td[1]/button').click()        
        
        # Operating Profit margin
        OPMcss = '#profit-loss > div.responsive-holder > table > tbody > tr:nth-child(4)'
        OPM = css2np(OPMcss,years)
        
        # Net Profit Margin
        NPMcss = '#profit-loss > div.responsive-holder > table > tbody > tr:nth-child(10)'
        NP = css2np(NPMcss,years)
        NPM = NP/sales*100
        NPM[NPM == -inf] = np.nan
        
        #Earnings Per Share
        EPScss = '#profit-loss > div.responsive-holder > table > tbody > tr:nth-child(11)'
        EPS = css2np(EPScss,years)
        
        #Debt
        Debtcss = '#balance-sheet > div > table > tbody > tr:nth-child(3)'
        Debt = css2np(Debtcss,years)
        
        # ROCE 
        ROCEcss = '#ratios > div > table > tbody > tr:nth-child(1)'
        ROCE = css2np(ROCEcss,years)
        
        #Operating and Investing CashFlows
        CFoperating_css = '#cash-flow > div > table > tbody > tr:nth-child(1)'
        CFoperating = css2np(CFoperating_css,years)
        
        
        # Assets purchased 
        dr.find_element_by_css_selector('#cash-flow > div.responsive-holder.fill-card-width > table > tbody > tr:nth-child(1) > td.text > button').click()
        AssetPur_css = '#cash-flow > div > table > tbody > tr:nth-child(3)'
        AssetPur = css2np(AssetPur_css,years)*-1
        AssetSold_css = '#cash-flow > div > table > tbody > tr:nth-child(4)'
        AssetSold = css2np(AssetSold_css,years)
        dr.find_element_by_css_selector('#cash-flow > div.responsive-holder.fill-card-width > table > tbody > tr.stripe.highlight.strong > td.text > button').click()
        
        # Reinvestment into bussiness
        Reinv_rate = AssetPur/ CFoperating * 100
        Reinv_rate[Reinv_rate<0] = 0
        
        # Free CashFlows
        FreeCashFlows = CFoperating-AssetPur+AssetSold
        
        #--------Fundamentals
        
        company = dr.find_element_by_css_selector(
            '#top > div.flex-row.flex-space-between.flex-gap-8 > h1').text.replace(' ', '_')
        Sector = dr.find_element_by_css_selector(
            '#peers > div.flex.flex-space-between > div:nth-child(1) > p').text
        MarCap = dr.find_element_by_css_selector(
            '#top-ratios > li:nth-child(1)').text.replace("\n"," ")
        year = years[0] - 1 if len(years) > 0 else 'NA'
        
        # a = dr.find_element_by_css_selector(
        #     '#top > div.company-info > div.company-ratios').text.split('\n')
        #PC = [x for x in a if 'Price to Free Cash Flow:' in x][0]
        
        # Plotting Trends
        plt.style.use('ggplot')
        fig, ax = plt.subplots(nrows=3, ncols=3,sharex=True)  #sharex=True
        fig.set_size_inches((30, 20))
        #fig.suptitle("Trends for "+company, fontsize=18)
        txt = company + '\n\n    ' + Sector + '    ' + MarCap + '    ' + 'Start Year: ' + str(year)
        
        fig.suptitle(txt, fontsize=18)
        
        # -------- Row 1
        
        # Sales Growth
        ax[0, 0].plot(years,SalesG, color='green')
        ax[0, 0].set_title('Sales growth %', fontsize=16)
        ax[0, 0].set_ylim(bottom=-20)
            
        # Operating profit margin
        ax[0, 1].plot( years,OPM, color='green')
        ax[0, 1].set_title('Operating Profit Margin in %', fontsize=16)
        ax[0, 1].set_ylim(bottom=-20)
               
        # Net- Profit Growth
        ax[0, 2].plot(years,NPM, color='green')
        ax[0, 2].set_title('Net profit growth %', fontsize=16)
        ax[0, 2].set_ylim(bottom=-20)
                
        
        # -------- Row 2
        
        # Asset Purchased
        ax[1, 0].plot(years, AssetPur, color='green')
        ax[1, 0].set_title('Asset Purchased in cr', fontsize=16)
        ax[1, 0].set_ylim(bottom=-20)        
        
        # Reinvestment rate
        ax[1, 1].plot(years, Reinv_rate, color='green') #dic2array(Asset_pur.keys())
        ax[1, 1].set_title('Reinvestment into Business in %', fontsize=16)
        ax[1, 1].set_ylim(bottom=0)
        
        
        # Return on capital invested
        ax[1, 2].plot(years, ROCE, color='green') #years,
        ax[1, 2].set_title('Return on Cap Employed in %', fontsize=16)
        ax[1, 2].set_ylim(bottom=-20)
            
        # -------- Row 3
        
        # Free Cash Flows
        ax[2, 0].plot(years,FreeCashFlows , color='green')
        ax[2, 0].set_title('Free Cash Flows', fontsize=16)
        ax[2, 0].set_ylim(bottom=-20)
        #ax[2, 0].set_ylim(-20,np.max(FreeCashFlows))
        
        # Debt
        ax[2, 1].plot(years, Debt, color='red')
        ax[2, 1].set_title('Debt in Cr', fontsize=16)
        
        
        # Earnings Per Sahre
        ax[2, 2].plot(years, EPS, color='green')
        ax[2, 2].set_title('EPS', fontsize=16)
        ax[2, 2].set_ylim(bottom=-20)
        #ax[2, 2].set_ylim(-20,np.max(EPS))
        
        plt.xticks(fontsize=12)
        plt.subplots_adjust(top=0.91)
        #plt.text(1, 1, txt, fontsize=16,transform=ax[1].transAxes)
        sec = Sector[0].replace('/', '~').split(':')[1].strip().replace(' ', '')
        plt.savefig('./TrendPlots/' + sec + '_' + company + '.png',
                    pad_inches=0.1,bbox_inches="tight")
        plt.close(fig)

dr.find_element_by_css_selector('#top-nav-menu > form > button').click()