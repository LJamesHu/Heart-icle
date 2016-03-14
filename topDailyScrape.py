from bs4 import BeautifulSoup
import requests
import datetime
import random
import time
import os

# First day with information
date = datetime.date(2014, 9, 10)
# Iterator to get next day
timeiter = datetime.timedelta(days=1)
today = datetime.date.today()

# Rotating list of user agents
agents = ['Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A']


def scrapeTop(day, dayFile):

    # Randomize user agent
    headers = {'User-Agent': agents[random.randint(0, 5)]}

    # Craft link using day
    link = "https://medium.com/top-stories/%s" % day

    # See if can scrape information (not broken)
    try:
        # Load and read information
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.content.decode('utf-8').encode('ascii', 'ignore'), 'html.parser')

        # Check if article exists, otherwise throw exception (bad practice)
        len(soup.find('article'))

        # Write if article exists
        with open('topdaily/' + dayFile + '.html', 'wb') as f:
            content = r.content.decode('utf-8').encode('ascii', 'ignore')
            f.write(content)

    # Print information on break, try again
    except:
        print 'Broke on %s' % day
        time.sleep(5)
        scrapeTop(day)

# Iterate until current day
while date != today:

    # Restructure date into month-day-year format for URL
    day = date.strftime('%B-%d-%Y').lower()

    # Restructure date into year-month-day for files for organization in file system
    dayFile = date.strftime('%Y-%m-%d')

    # Iterate the day
    date += timeiter

    # If already scraped, should exist in directory, then skip
    if os.path.exists('topdaily/' + dayFile + '.html'):
        continue

    scrapeTop(day, dayFile)

    # Sleep some to slow down number of hits on server
    time.sleep(random.randint(3, 15))

raw_input('Finished.')