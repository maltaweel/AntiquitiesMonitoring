'''
Created on Feb 17, 2020

@author: mark
'''

import geocoder
from geopy.geocoders import Nominatim
import time


from geopy.extra.rate_limiter import RateLimiter

import os

import csv
import analysis.sendEmail as sendEmail

geolocator = Nominatim(user_agent="specify_your_app_name_here")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

done=[]
def getState(location):
   
    g = geocoder.osm(location)
    time.sleep(2)
    return g.state


'''
The file output path for printing results (to the src level of this project)
@return rn- the output file path to use to the src level
''' 
def filenameToOutput():
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        
        return pn

def findLocation(writer,csvf):
    sendEmail=False
    filename=os.path.join(filenameToOutput(),'output','scrapedOutput.csv')
    keepRows=[]
    try:
        with open(os.path.join(filename),'rU') as csvfile:
            reader = csv.DictReader(csvfile)
            
            i=0
            for row in reader:
                 
                location=row['Location']
                state=getState(location)
                if state is None:
                    i+=1
                    continue
                
                print(state)
                if "Scotland" in state:
                    obj=row['Object']
                    prc=row['Price']
                    if obj+":"+prc in done:
                        continue
                    else:
                        done.append(obj+":"+prc)
                    printResults(row,writer)
                    sendEmail=True
                    csvf.flush()
            
                i+=1
            return keepRows     
                 
            
    except IOError:
        print ("Could not read file:", csvfile)
        
    return sendEmail
            
def printResults(row,writer):
        
    
      
            
    obj=row['Object']
    prc=row['Price']
    loc=row['Location']
    sel=row['Seller']
    img=row['Image']
    lnk=row['Link']
            
    writer.writerow({'Object': str(obj),'Price':str(prc),'Location':str(loc),'Seller':str(sel),'Image':str(img),'Link':str(lnk)})
    
            
'''
Method to run the module and launch the analysis
'''                    
def run():
    
    fieldnames = ['Object','Price','Location','Seller','Image','Link']

    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    #output is namedEntityMerged.csv
    fileOutput=os.path.join(pn,'output',"scotlandFinds.csv")
    
    #opens the output file and then puts the output in
    with open(fileOutput, 'wt') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()  
        
        #first load any data we need and find location
        runEmail=findLocation(writer,csvf)
    
        csvf.flush()
    #   if runEmail==True:
    #       sendEmail.run()

        print("Finished")
   
if __name__ == '__main__':
    run()