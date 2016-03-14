from bs4 import BeautifulSoup
import os

# List of top dailies
dailylist = os.listdir('topdaily/')

articles = set()

# Iterate
for file in dailylist:

    # Open top daily files
    with open('topdaily/' + file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Pull block with article link
    blocks = soup.findAll('div', {'class': 'block block--inset block--list block--preview cardChromeless js-block js-trackedPost postItem js-postItem'})

    # Get link from aforementioned block
    links = [block.find('a', {'class': 'link link--darken'})['href'].split('?source')[0] for block in blocks if 'K' in block.find('button', {'data-action': 'show-recommends'}).get_text() or int(block.find('button', {'data-action': 'show-recommends'}).get_text().strip('K')) > 200]

    # Add link to set
    articles.update(links)

# Print set to a list of articles
with open('articleList.txt', 'wb') as articleList:
    articleList.write('\n'.join(articles))