from bs4 import BeautifulSoup
import multiprocessing
import numpy as np
import unidecode
import os
import re

def article_processd2v(file):

    # Open the article
    with open('../train/' + file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Get top highlight
    highlight = soup.find('span', {'data-creator-ids': 'anon'})
    highlightClean = unidecode.unidecode(" ".join(item.strip() for item in highlight.find_all(text=True)))

    highlightClean = highlightClean.lower()
    highlightClean = re.sub('\.', ' . ', highlightClean)
    highlightClean = re.sub('\"', ' " ', highlightClean)
    highlightClean = re.sub('\,', ' , ', highlightClean)
    highlightClean = re.sub('\(', ' ( ', highlightClean)
    highlightClean = re.sub('\)', ' ) ', highlightClean)
    highlightClean = re.sub('\!', ' ! ', highlightClean)
    highlightClean = re.sub('\?', ' ? ', highlightClean)
    highlightClean = re.sub('\:', ' : ', highlightClean)
    highlightClean = re.sub('\;', ' ; ', highlightClean)
    highlightClean = re.sub('\-\-', ' -- ', highlightClean)
    highlightClean = highlightClean.strip()

    # Go to class containing article
    article = soup.find('main', {'class': 'postArticle-content js-postField js-notesSource'})

    # Strip out special tag that adds bad information
    [x.extract() for x in article.find_all('noscript')]
    [x.extract() for x in article.find_all('h1')]
    [x.extract() for x in article.find_all('h2')]
    [x.extract() for x in article.find_all('h3')]
    [x.extract() for x in article.find_all('h4')]
    [x.extract() for x in article.find_all('h5')]
    [x.extract() for x in article.find_all('h6')]

    # Get text information, clean up unicode
    articleClean = unidecode.unidecode(" ".join(item.strip() for item in article.find_all(text=True)))

    articleClean = articleClean.lower()
    articleClean = re.sub('\.', ' . ', articleClean)
    articleClean = re.sub('\"', ' " ', articleClean)
    articleClean = re.sub('\,', ' , ', articleClean)
    articleClean = re.sub('\(', ' ( ', articleClean)
    articleClean = re.sub('\)', ' ) ', articleClean)
    articleClean = re.sub('\!', ' ! ', articleClean)
    articleClean = re.sub('\?', ' ? ', articleClean)
    articleClean = re.sub('\:', ' : ', articleClean)
    articleClean = re.sub('\;', ' ; ', articleClean)
    articleClean = re.sub('\-\-', ' -- ', articleClean)
    articleClean = articleClean.strip()

    return [highlightClean, articleClean]

if __name__ == '__main__':

    # List of articles
    articles = os.listdir('../train/')

    # Setup multiprocessing
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)

    # Process articles for w2v
    w2vArticles = np.array(pool.map(article_processd2v, articles))

    with open('../highlights.txt', 'wb') as highlights:
        for highlight in w2vArticles[:, 0]:
            highlights.write("%s\n" % highlight)

    with open('../articles.txt', 'wb') as articles:
        for article in w2vArticles[:, 1]:
            articles.write("%s\n" % article)