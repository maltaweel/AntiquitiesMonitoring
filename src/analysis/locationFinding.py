'''
Created on Feb 17, 2020

@author: mark
'''

import geocoder
import os

import csv


def getState(location):

    g = geocoder.osm(location)

    return g.state


'''
The file output path for printing results (to the src level of this project)
@return rn- the output file path to use to the src level
''' 
def filenameToOutput():
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        
        return pn

def findLocation():
    filename=os.path.join(filenameToOutput(),'output','scrapedOutput.csv')
    keepRows=[]
    try:
        with open(os.path.join(filename),'rU') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                 
                location=row['Location']
                state=getState(location)
                if state is None:
                    continue
                
                if "Scotland" in state:
                    keepRows.append(row)
            
            
            return keepRows     
                 
            
    except IOError:
        print ("Could not read file:", csvfile)
            
def printResults(keepRows):
    
    fieldnames = ['Object','Price','Location','Seller','Image','Link']

    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    #output is namedEntityMerged.csv
    fileOutput=os.path.join(pn,'output',"scotlandFinds.csv")
    
    #opens the output file and then puts the output in
    with open(fileOutput, 'wt') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
    
        for i in keepRows:
            
            obj=i['Object']
            prc=i['Price']
            loc=i['Location']
            sel=i['Seller']
            img=i['Image']
            lnk=i['Link']
            
            writer.writerow({'Object': str(obj),'Price':str(prc),'Location':str(loc),'Seller':str(sel),'Image':str(img),'Link':str(lnk)})
            
            
'''
Method to run the module and launch the analysis
'''                    
def run():
    
    #first load any data we need and find location
    keepRows=findLocation()
    
    printResults(keepRows)

    print("Finished")
   
if __name__ == '__main__':
    run()