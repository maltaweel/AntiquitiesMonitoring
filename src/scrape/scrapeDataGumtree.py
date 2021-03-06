'''
Created on Feb 15, 2020

@author: mark
'''
from bs4 import BeautifulSoup
import os
import csv
import requests
import urllib.request
from urllib.request import urlopen
import datetime
import math
from scrape.scrapeDataUKEbay import price
import time

from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

baseUrl = 'https://www.gumtree.com/'
search_arg = 'search?'
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/51.0.2704.103 Safari/537.36'}

        
url1='http://www.gumtree.com/search?featured_filter=false&urgent_filter=false&sort=date&search_scope=false&photos_filter=false&search_category=all&q='
url2='&tq=&search_location='

part1=['antiques']
part2=['Scotland']

prices={}
links={}
images={}
locations={}
users={}

webdriver = os.path.join(os.path.abspath(__file__).split('src')[0],'chromedriver')

#driver = Chrome(webdriver)

#wait = WebDriverWait(driver, 10)
            
'''
The file output path for printing results (to the src level of this project)
@return rn- the output file path to use to the src level
''' 
def filenameToOutput():
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        
        return pn

def make_urls():

    urls = []
    
    for p in part1:
        url=url1+str(p)
                
        for pp in part2:
            url=url+url2+str(pp)
              
            run=True
            for i in range(1,10000000):
                if run==False:
                    break
                run=gumtree_scrape(url,p,pp)
        
        
def gumtree_scrape(urlFull,p,pp):
    
    '''
    <h2 class="listing-title">

    <a class="listing-link "
    href="/p/antiques/antique-authentic-french-dresser/1367713977">

    <div class="listing-side">
    <div class="listing-thumbnail">
'''
    # Downloads the eBay page for processing
    originalUrl=urlFull
            
    run=True
    
    '''      
        for item in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "listing-title"))):
            company_name = item.find_element_by_id("company-name-1").text
            ceo_name = item.find_element_by_id("ceo-name-1").text
            print(company_name,ceo_name)

        driver.quit()
    '''       
    
    while(run):

        print(originalUrl)
        time.sleep(2)
        r=requests.get(originalUrl,headers=header)
        time.sleep(2)
   
        soup=BeautifulSoup(r.text, 'html.parser') 
        num=soup.find_all('h2',{"class":'listing-title'})
        nnt=soup.find_all("a", {"class":'listing-link'})
        ntt=soup.find_all("div", {"class":'listing-thumbnail'})
        
        for n in nnt:
            href=n['href']
            if href=="":
                continue
            
            href="https://www.gumtree.com"+href
            time.sleep(2)
            resS = requests.get(href,headers=header)
            time.sleep(2)
            soupS = BeautifulSoup(resS.text, 'html.parser')
            title=soupS.find_all("title")
            price=soupS.find_all("strong",{'class':"ad-price txt-xlarge txt-emphasis inline-block"})

            prce=''
            ttle=''
            for t in title:
                ttle=t
            
            for p in price:
                prce=p
                

if __name__ == '__main__':
    fieldnames = ['Object','Date','Price','Location','Seller','Ad ID','Image','Link']
    
    
    filename=os.path.join(filenameToOutput(),'output','scrapedGumtreeOutput.csv')
    
    #here we open the results which will the name of cultures scraped from eBay
    with open(filename, 'wt') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()  
        make_urls()
    
        print('Finished')