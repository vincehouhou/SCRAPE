
# ************************************************************************
# File:    google.py
# Purpose: scrape google search results
# Author:  Houdong Hu
# ************************************************************************

from BeautifulSoup import BeautifulSoup
from datetime import datetime
import urllib, urllib2
import re

def google_scrape(query):
    t1 = datetime.now()
    address = "http://www.google.com/search?q=%s&num=100&hl=en&start=0" % (urllib.quote_plus(query))
    request = urllib2.Request(address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    urlfile = urllib2.urlopen(request)
    page = urlfile.read()
    t2 = datetime.now()
   
    soup = BeautifulSoup(page)
 
    linkdictionary = {}

    li = soup.find('li', attrs={'class':'g'})
    
    rDiv = li.find('h3', attrs={'class':'r'})
    rDiv1 = re.compile(r'<.*?>').sub('',str(rDiv)).replace('.','')
    print rDiv1
        
    sLink = li.find('a')
    slink1 = sLink['href']
    print slink1

    fDiv = li.find('div', attrs={'class':'f slp'})
    fDiv1 = re.compile(r'<.*?>').sub('',str(fDiv)).replace('.','').replace('&nbsp','').replace('-;','').replace(';Rating','Rating')
    print fDiv1

    sSpan = li.find('span', attrs={'class':'st'}) 
    sSpan1 = re.compile(r'<.*?>').sub('',str(sSpan)).replace('.','')
    print sSpan1

    t3 = datetime.now() 
    
    print "Scraping Time is ", t2-t1
    print "parsing time is ", t3-t2
    return linkdictionary

if __name__ == '__main__':
    links = google_scrape("7770 Vickers St Ste 101 (at Convoy St)  San Diego, CA 92111 site:yelp.com")

