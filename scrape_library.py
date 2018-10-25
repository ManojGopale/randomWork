## scrape library website to retrieve the number of laptops available to loan
## Need to check how this data can be viewed easily (Mailing when the available laptops are more than 2, so as to renew)
## Creating a cron job that runs this command indefinitly so that emails are received.

import requests
from bs4 import BeautifulSoup

## Returns a tuple of libraryName and numLaptops in each library
def getInfo(soup):
	## Search for div with the availability info from webpage
	search = soup.find_all('div', {'class': 'field-name-field-eq-availability-display'})
	
	#print(search)
	#print("length= %s" %(len(search)))
	
	#print("search[0]= %s" %(search[0]))
	
	avail1 = search[0].find_all('div', {'class': 'even'})
	#print("avail1 = %s" %(avail1))
	
	## get all divs inside the search and go to the div with 'class' 'even', this has the number of 
	## laptops available to loan
	numLaptops = [avail.text for divs in search for avail in divs.find_all('div', {'class', 'even'})]
	
	
	## get all the divs with library name
	searchLib = soup.find_all('div', {'class': 'field-name-field-eq-location'})
	
	## Search through the div's inside searchLib to get div with class 'even' which has the library names
	libName = [lib.text for divs in searchLib for lib in divs.find_all('div', {'class': 'even'})]
	
	#print(numLaptops)
	#print(libName)
	#
	#for num, library in zip(numLaptops, libName):
	#	print ("%s, %s" %(num, library))

	return (numLaptops, libName)


## Get the webpage for mac and pc from UoA webpages
macData = requests.get('http://new.library.arizona.edu/tech/borrow/macbook')
pcData = requests.get('http://new.library.arizona.edu/tech/borrow/pc-laptop')

## Soup is now an object of the html page retrieved
macSoup = BeautifulSoup(macData.text, 'html.parser')
pcSoup = BeautifulSoup(pcData.text, 'html.parser')

macNum, macLib = getInfo(macSoup)
pcNum, pcLib = getInfo(pcSoup)

print("\n####### Mac #########")
for num, library in zip(macNum, macLib):
	print("%s, %s" %(num, library))

print("\n###### PC ##########")
for num, library in zip(pcNum, pcLib):
	print("%s, %s" %(num, library))
