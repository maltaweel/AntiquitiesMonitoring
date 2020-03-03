'''
Created on Feb 15, 2020

@author: mark
'''
from bs4 import BeautifulSoup
import os
import csv
import requests
from urllib.request import urlopen
import datetime
import math
from selenium import webdriver
from scrape.scrapeDataUKEbay import price

baseUrl = 'https://www.gumtree.com/'
search_arg = 'search?'
USER_AGENT = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"
REQUEST_HEADERS = {'User-agent': USER_AGENT,}
        
url1='http://www.gumtree.com/search?featured_filter=false&urgent_filter=false&sort=date&search_scope=false&photos_filter=false&search_category=all&q='
url2='&tq=&search_location='

part1=['antiques']
part2=['Scotland&tl=']

prices={}
links={}
images={}
locations={}
users={}

            
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
    
    while(run):

        print(originalUrl)
    #    request = requests.get("http://www.gumtree.com/search?q=%s&search_location=%s&category=%s" % ("", p, pp),headers=REQUEST_HEADERS)
        request=requests.get(originalUrl)
        
        ''''
        # Raises an exception error if there's an error downloading the website
        try:
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            run=False
        '''    
           
        # Creates a BeautifulSoup object for HTML parsing
        soup = BeautifulSoup(request.text, 'html5lib')
            
        num=soup.find_all('h2',{"class":'listing-title'})
        nnt=soup.find_all("a", {"class":'listing-link'})
        ntt=soup.find_all("div", {"class":'listing-thumbnail'})
        
        for n in nnt:
            
            resS = requests.get(n)
#            print(s)
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