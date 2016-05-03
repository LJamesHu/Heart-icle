from bs4 import BeautifulSoup
import os

# List of article indexers
articleIndex = os.listdir('articleIndex/')

articles = set()

# Iterate
for file in articleIndex:

    # Open top daily files
    with open('articleIndex/' + file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Pull links from latest page
    blocks = soup.find('ul', {'class': 'river'}).findAll('a', {'data-omni-click': 'inherit'})
    links = ['http://www.theatlantic.com' + block['href'] for block in blocks if 'archive' in block['href']]

    # Add link to set
    articles.update(links)

# Print set to a list of articles
with open('articleList.txt', 'wb') as articleList:
    articleList.write('\n'.join(articles))