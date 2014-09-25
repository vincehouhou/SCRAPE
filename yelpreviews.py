
# ************************************************************************
# File:    yelpreviews.py
# Purpose: 3 python classes to get yelp business links, yelp business infos and yelp business reviews separately are created 
# Author:  Houdong Hu
# ************************************************************************


import urllib2
from BeautifulSoup import BeautifulSoup
from xml.sax.saxutils import unescape
from unicodedata import normalize
import json
import sys
import time
import logging
logging.basicConfig(format = "[%(asctime)s] %(message)s",
                    datefmt='%a %b %d %H:%M:%S %Y',
                    level = logging.DEBUG)

def gettext(entry):
    if entry:
        return normalize2(entry.text)
    else:
        return "" 

def normalize2(text):
    return text.encode('ascii','ignore').replace("|","[bar]").replace('\n',' ')
   

def getsoup(link, logger, bizID, small_gap=5, max_num_try=3):
    
    num_try = 0
    gap=0
    soup=''
    while num_try <= max_num_try:
        time.sleep(gap)
        gap += small_gap
        num_try += 1
        try:
            result=urllib2.urlopen(link)
        except urllib2.HTTPError, e:
            logger.info("bizID{0:010d}: -------> HTTP Error: server available but failed request:{1}".format(int(bizID),e.code))
        except urllib2.URLError, e:
            logger.info("bizID{0:010d}: -------> URL Error: server unavailable. Reason:{1}".format(int(bizID),e.code))
            logger.info("Retry in {0} seconds...".format(gap))
        except:
            logger.info("Error to open the internet page")
        else:
            num_try=max_num_try+1
            soup=BeautifulSoup(result.read())

    if not soup: 
        logger.info("bizID{0}: don't get biz information".format(bizID))
       
    return soup

class getlinks:
    def __init__(self,conf,logger,outputfile):
        self.url=conf["url"]
        self.pagestart=conf["getlinks_pagestart"]
        self.pageend=conf["getlinks_pageend"]
        self.logger=logger
        self.outputfile=outputfile

    def getbizlinks(self):
        prefix='http://www.yelp.com'
        for i in range(self.pagestart,self.pageend):
            bizID=i*10+1
            pageurl=self.url+'&start='+str(10*i)
            soup=getsoup(pageurl,self.logger,bizID)
            if soup:
                bizlinks=soup.findAll('span',attrs={'class':'indexed-biz-name'})
                links=[prefix+bizlink.find('a')['href'].encode('ascii') for bizlink in bizlinks]
                for link in links:
                    link.replace('|','[bar]')
                    self.outputfile.write('|'.join([str(bizID),link]))
                    self.outputfile.write('\n')
                    bizID=bizID+1


class getreviews:
    def __init__(self,link,logger,bizID):
        self.link=link
        self.logger=logger
        self.bizID=bizID
        self.soup=''
        self.numreview=0
        self.reviewlist=[]

    def getbizinfo(self):
        self.soup=getsoup(self.link,self.logger,self.bizID)
        if self.soup:
            self.numreview=gettext(self.soup.find('span',itemprop='reviewCount'))

    def getbizreviews(self):
        if self.numreview:
            for i in range(0,int(self.numreview),40):
                reviewlink=self.link+'?start='+str(i)
                reviewpage=getsoup(reviewlink,self.logger,self.bizID)
                reviews=[]
                try:
                    reviews=reviewpage.find('div',id='bizReviews').find('div',id='reviews-other').findAll('li',itemprop='review')
                except:
                    try:
                        reviews=reviewpage.findAll('div',attrs={'class':'review-content'})
                    except:
                        self.logger.info("bizID{0:010d}: can not find reviews on review {1}...".format(int(bizID),i))

                for r in reviews:
                    itemrating=r.find('meta',itemprop='ratingValue')
                    if itemrating:
                        rating=normalize2(itemrating.get('content',''))
                        itemdate=r.find('meta',itemprop='datePublished')
                    if itemdate:
                        date=normalize2(itemdate.get('content',''))
                    comment=gettext(r.find('p',itemprop='description'))
                    self.reviewlist.append(yelpreview(rating,date,comment))

    def dumpbizreviews(self,outputfile):
        for r in self.reviewlist:
            print >> outputfile, "|".join([self.bizID,r.rating,r.date,r.comment])

class getinfos:
    def __init__(self,link,logger,bizID,conf):
        self.link=link
        self.logger=logger
        self.bizID=bizID
        self.conf=conf
        self.name=''
        self.numreview=''
        self.rating=''
        self.street=''
        self.city=''
        self.state=''
        self.zip=''
        self.phone=''
        self.bizurl=''
        self.categories=[]

    def getbizinfos(self):
        
        self.soup=getsoup(self.link,self.logger,self.bizID)

        if self.soup: 
           
            self.numreview=gettext(self.soup.find('span',itemprop='reviewCount'))
            self.name=gettext(self.soup.find('h1',itemprop='name'))
            
            itemrate=self.soup.find('meta',itemprop='ratingValue')
            if itemrate:
                self.rating=normalize2(itemrate.get('content',''))

            cat_display=self.soup.find('span',id='cat_display')
            if cat_display:
                self.categories=[normalize2(c.text).replace(',',' ') for c in cat_display.findAll('a')]

            address=self.soup.find('address',itemprop='address')
            if address:
                self.street=gettext(address.find('span',itemprop='streetAddress'))
                self.city=gettext(address.find('span',itemprop='addressLocality'))
                self.state=gettext(address.find('span',itemprop='addressRegion'))
                self.zip=gettext(address.find('span',itemprop='postalCode'))

            self.phone=gettext(self.soup.find('span',id='bizPhone',itemprop='telephone'))
            bizUrl=self.soup.find('div', id='bizUrl')
            if bizUrl:
                self.bizurl=gettext(bizUrl.find('a'))

    def dumpbizinfos(self,outputfile):
        bizcategories=",".join([c for c in self.categories])
        bizinfos="|".join([str(self.bizID),self.link,self.name,self.numreview,self.rating,self.street,self.city,self.state,self.zip,self.phone,self.bizurl,bizcategories])
        print >> outputfile, bizinfos

            
class yelpreview:
    def __init__(self,rating,date,comment):
        self.rating=rating
        self.date=date
        self.comment=comment.encode('ascii')


