from bs4 import BeautifulSoup
import cPickle as pickle
import pandas as pd
import unidecode
import os


dfArticles = pd.DataFrame()

# List all files in the directory to travel down
articles = os.listdir('highlightArticles/')

for file in articles:

    # Open file
    with open('highlightArticles/' + file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Find title, remove Medium bit, cleanup unicode
    title = unidecode.unidecode(soup.find('title').get_text()).strip(' - Medium')

    # Go to class containing article
    article = soup.find('main', {'class': 'postArticle-content js-postField js-notesSource'})
    # Strip out special tag that adds bad information
    [x.extract() for x in article.find_all('noscript')]
    # Get text information, clean up unicode
    articleClean = unidecode.unidecode(" ".join(item.strip() for item in article.find_all(text=True)))

    # Find quote, cleanup unicode
    quote = unidecode.unidecode(soup.find('span', {'data-creator-ids': 'anon'}).get_text())

    # Add to temporary dataframe for appending
    dfTemp = pd.DataFrame({'title': [title], 'article': [articleClean], 'quote': [quote]})

    # Add to df
    dfArticles = dfArticles.append(dfTemp)

print dfArticles

# Pickle data for easy recall
with open('dfArticles.pkl', 'w') as pkl:
    pickle.dump(dfArticles, pkl)