
# ************************************************************************
# File:    scrapeyelp.py
# Purpose: scrape yelp business infos, and takes use of ''yelpreviews.py'' mainly
# Author:  Houdong Hu
# ************************************************************************


import urllib2
from BeautifulSoup import BeautifulSoup
from xml.sax.saxutils import unescape
from unicodedata import normalize
from yelpreviews import *
import json
import sys
import os
import gzip
import time
TIME_FORMAT = '%a %b %d %H:%M:%S %Y'
import logging
logging.basicConfig(format = "[%(asctime)s] %(message)s",
                    datefmt='%a %b %d %H:%M:%S %Y',
                    level = logging.DEBUG)

class Logger:
    def __init__(self, writer=sys.stderr):
        self._writer = writer

    def __del__(self):
        self._writer.close()

    def info(self, *args):
        print >>self._writer, "[{0}] {1}".format(
            time.strftime(TIME_FORMAT),
            " ".join([str(msg) for msg in args]))

def loadConfig(confFile):
    with open(confFile) as f:
        lines = f.readlines()
        pairs = [line.strip().split(":",1) for line in lines]
        strJSON = ",\n".join(['"{0}": {1}'.format(
            pair[0].replace('"','').replace("'",''),
            pair[1].replace("'",'"')) for pair in pairs])
        conf = json.loads("{" + strJSON + "}")

    return conf

def getyelplinks(conf):

    if "links_folder" not in conf:
        logging.info("no links_folder provided")
        exit(1)
    else:
        links_folder = conf["links_folder"]
    if not os.path.exists(links_folder):
        os.makedirs(links_folder)
    
    dirname=conf["links_folder"]
    os.chdir(dirname)
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    logFile =  "logs/yelp_reviews_" + time.strftime("%Y.%m.%d_%H.%M.%S") + ".log.gz"
    logger = Logger(gzip.open(logFile,"wb"))

    filename="{0}_page_{1}_{2}".format(conf["links_folder"],conf["getlinks_pagestart"],conf["getlinks_pageend"])

    with open(filename,'w') as outputfile:
        logging.info("Create file "+filename)
        print >> outputfile, "bizID|yelpurl"
        biz=getlinks(conf,logger,outputfile)
        biz.getbizlinks()

    logger.info("Done")

def getyelpreviews(conf):

    if "reviews_folder" not in conf:
        logging.info("no reviews_folder provided")
        exit(1)
    else:
        reviews_folder = conf["reviews_folder"]
    if not os.path.exists(reviews_folder):
        os.makedirs(reviews_folder)
    
    dirname=conf["reviews_folder"]
    os.chdir(dirname)
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    logFile =  "logs/yelp_reviews_" + time.strftime("%Y.%m.%d_%H.%M.%S") + ".log.gz"
    logger = Logger(gzip.open(logFile,"wb"))

    with open("../"+conf["links_file"]) as links:

        count=0          
        outputfile = None 

        links.readline()
        for i in range(conf["getreviews_bizstart"]-1):
            links.readline()

        for link in links:
            items=link.rstrip().split("|")
            bizID=items[0]
            link=items[1]
            reviews=getreviews(link,logger,bizID)
            reviews.getbizinfo()
            reviews.getbizreviews()
            
            if count >= conf['reviews_venue_per_file']:
                count = 0
                if outputfile:
                    outputfile.close()

            count += 1

            if count == 1:
                outputfile = gzip.open("{0}_{1:010d}.gz".format(dirname, int(bizID)), "wb")
                logging.info("Create file "+"{0}_{1:010d}.gz".format(dirname, int(bizID)))
                print >> outputfile,"bizID|rating|date|review"
            
            reviews.dumpbizreviews(outputfile)

        outputfile.close()
        
    logger.info("Done")

def getyelpinfos(conf):

    if "infos_folder" not in conf:
        logging.info("no infos_folder provided")
        exit(1)
    else:
        infos_folder = conf["infos_folder"]
    if not os.path.exists(infos_folder):
        os.makedirs(infos_folder)

    dirname=conf["infos_folder"]
    os.chdir(dirname)
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    logFile =  "logs/yelp_infos_" + time.strftime("%Y.%m.%d_%H.%M.%S") + ".log.gz"
    logger = Logger(gzip.open(logFile,"wb"))

    with open("../"+conf["links_file"]) as links:

        count=0          
        outputfile = None 

        links.readline()
        for i in range(conf["getinfos_bizstart"]-1):
            links.readline()

        for link in links:

            items=link.rstrip().split("|")
            bizID=items[0]
            link=items[1]
            infos=getinfos(link,logger,bizID,conf)
            infos.getbizinfos()
            
            if count >= conf['infos_venue_per_file']:
                count = 0
                if outputfile:
                    outputfile.close()

            count += 1
            if count == 1:
                outputfile = gzip.open("{0}_{1:010d}.gz".format(dirname, int(bizID)), "wb")
                logging.info("Create file "+"{0}_{1:010d}.gz".format(dirname, int(bizID)))
                print >> outputfile, "bizID|yelpurl|name|numreview|rating|street|city|state|zip|phone|url|categories"
                
            infos.dumpbizinfos(outputfile)

        outputfile.close()
        
    logger.info("Done")


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print >>sys.stderr, "Funtion name and configuration file are not given."
        exit(1)

    if len(sys.argv) < 3:
        print >>sys.stderr, "Configuration file not given."
        exit(1)

    conf = loadConfig(sys.argv[2])

    funcName = sys.argv[1]
    allVars = locals()
    if funcName in allVars:
        allVars[funcName](conf)
    else:
        logging.info("Can't find function `{0}'".format(funcName));
  
