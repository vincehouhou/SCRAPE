
# ************************************************************************
# File:    bing.py
# Purpose: scrape bing searching results
# Author:  Houdong Hu
# ************************************************************************


import urllib,urllib2
import re
from BeautifulSoup import BeautifulSoup
from datetime import datetime
   
def bing_grab(query):   
    t1 = datetime.now()
    address = "http://www.bing.com/search?q=%s" % (urllib.quote_plus(query)) 

    request = urllib2.Request(address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    urlfile = urllib2.urlopen(request)
    page = urlfile.read()
    soup = BeautifulSoup(page)
    t2 = datetime.now()


    linkdictionary = {}

    # 'li' has two kinds of classed 'sa_wr wr_at' and 'sa_wr'
    li = soup.find('li', attrs={'class': re.compile(r".*\bsa_wr\b.*")})
    h3 = li.find('h3')
    h31 = re.compile(r'<.*?>').sub('',str(h3)).replace('.','')
    print h31

    sLink = li.find('a')
    slink1 = sLink['href']
    print slink1

    Cite = li.find('cite')
    Cite1 = re.compile(r'<.*?>').sub('',str(Cite))
    Cite2 = re.compile(r'&.*?;').sub(' ',str(Cite1))
    print Cite2

    # Rating = li.find('span', attrs={'class':'ssp_ylp'})
    # print Rating

    Info = li.find('ul', attrs={'class':'sp_pss'})
    Info1 = re.compile(r'<.*?>').sub('',str(Info))
    Info2 = re.compile(r'&.*?;').sub(' ',str(Info1))
    print Info2

    P = li.find('p')
    P1 = re.compile(r'<.*?>').sub('',str(P))
    P2 = re.compile(r'&.*?;').sub(' ',str(P1))
    print P2

    t3 = datetime.now()

    print "Scraping Time is ", t2-t1
    print "parsing time is ", t3-t2
    return linkdictionary


    return linkdictionary

if __name__ == '__main__':
    links = bing_grab("tea station yelp")
  
