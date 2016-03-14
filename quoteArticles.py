from bs4 import BeautifulSoup
import os

# List of articles
articles = os.listdir('articles/')

# Iterate
for file in articles:

    # If the file has been processed and has a top highlight, should already be in directory
    if os.path.exists('highlightArticles/' + file):
        continue

    # Open the article
    with open('articles/' + file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Check if it has a top highlight
    highlight = soup.find('span', {'data-creator-ids': 'anon'})

    # If it has a highlight, add it to highlightArticles folder
    if highlight != None:
        with open('highlightArticles/' + file, 'wb') as f2:
            f2.write(str(soup))