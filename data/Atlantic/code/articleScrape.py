import requests
import random
import time
import os

# Rotating list of user agents
agents = ['Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A']

# Open list of articles that need to be scraped
with open('../articleList.txt') as f:
    articles = f.read().split()

# Iterate
for article in articles:

    # Randomize user agent
    headers = {'User-Agent': agents[random.randint(0, 5)]}

    # Check if already scraped with file existing
    if os.path.exists('../articles/' + article.split('/')[-3] + '-' + article.split('/')[-2] + '.html'):
        continue

    # Load and read information
    r = requests.get(article, headers=headers)

    # Save file
    with open('../articles/' + article.split('/')[-3] + '-' + article.split('/')[-2] + '.html', 'wb') as f2:
        f2.write(r.content)

    # Sleep some to slow down number of hits on server
    time.sleep(random.randint(2, 4))