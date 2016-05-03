from bs4 import BeautifulSoup
import requests
import datetime
import random
import time
import os

# Rotating list of user agents
agents = ['Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A']


def scrapeIndex(page):

    # Randomize user agent
    headers = {'User-Agent': agents[random.randint(0, 5)]}

    # Craft link using day
    link = "http://www.theatlantic.com/latest/?page=%s" % page

    # See if can scrape information (not broken)
    try:
        # Load and read information
        r = requests.get(link, headers=headers)

        # Write if article exists
        with open('articleIndex/page' + format(page, '03') + '.html', 'wb') as f:
            f.write(r.content)

    # Print information on break, try again
    except:
        print 'Broke on %s' % page
        time.sleep(5)
        scrapeIndex(page)

page = 1
while page < 1000:

    if os.path.exists('articleIndex/page' + format(page, '03') + '.html'):
        page += 1
        continue

    scrapeIndex(page)

    page += 1

    # Sleep some to slow down number of hits on server
    time.sleep(random.randint(2, 4))

raw_input('Finished.')