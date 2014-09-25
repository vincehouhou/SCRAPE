
*****************************************************************************************
A. YELP REVIEWS SCRAPING

# I developed the yelp reviews scraping code based on Lingyun Zhang and Shengjun Pan's previous work. #

You also need to specify a configuration file 0.conf (we have an example file in this directory). Here is the dictionary of fields in the configuration file:

Get business links:
url: The first pape of your yelp searching result. For example: "http://www.yelp.com/search?find_desc=&find_loc=San+Diego%2C+CA&ns=1" is the first page of yelp business searching results in San Diego.
getlinks_pagestart: start pape of your yelp searching result.
getlinks_pageend: end page of your yelp searching result.
links_folder: where your business links output file will be saved.
Get business infos:
links_file: yelp business links file which you get it by running "get business links" code.
getreviews_bizstart: you will start from which business in links_file.
infos_venue_per_file: how many businesses in each output file.
infos_folder: where your business infos output file will be saved.
Get business reviews:
links_file: yelp business links file which you get it by running "get business links" code.
getreviews_bizstart: you will start from which business in links_file.
reviews_venue_per_file: how many businesses in each output file.
reviews_folder: where your business reviews output file will be saved.
Run The Code

python scrapeyelp.py getyelplinks 0.conf: get business yelp links
python scrapeyelp.py getyelpreviews 0.conf: get business yelp reviews
python scrapeyelp.py getyelpinfos 0.conf: get business yelp infos
Log File

There will be a log file generated in corresponding folder once you run the code.

*****************************************************************************************
B. GOOGLE SEARCHING RESULTS SCRAPING

How to run the code:

python google.py google_scrape
You could setup your searching content here:

if __name__ == '__main__':
  links = google_scrape("7770 Vickers St Ste 101 (at Convoy St)  San Diego, CA 92111 site:yelp.com")

*****************************************************************************************
C. BING SEARCHING RESULTS SCRAPING

How to run the code:

python bing.py bing_grab
You could setup your searching content here:

if __name__ == '__main__':
  links = bing_grab("tea station yelp")
