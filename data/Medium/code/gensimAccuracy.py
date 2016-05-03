from gensim.summarization import summarize
from bs4 import BeautifulSoup
import multiprocessing
import unidecode
import os
import re


def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]


def articleGensim(file):

    # Open the article
    with open('../validArticles/' + file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Check if it has a top highlight
    highlight = soup.find('span', {'data-creator-ids': 'anon'})

    # Clean up highlight and remove bad unicode
    highlightClean = unidecode.unidecode(" ".join(item.strip() for item in highlight.find_all(text=True)))

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

    articleClean = unidecode.unidecode(" ".join(item.strip() for item in article.find_all(text=True)))

    # Summarize article using TextRank
    summary = summarize(articleClean, word_count=100)

    # Remove formatting so format anomalies don't affect results
    highlightNoFormat = re.sub("[^a-zA-Z]", "", highlightClean)
    summaryNoFormat = re.sub("[^a-zA-Z]", "", summary)

    if len(longest_common_substring(summaryNoFormat, highlightNoFormat)) > min(len(summaryNoFormat), len(highlightNoFormat)) - 10:
        return 1
    else:
        return 0

if __name__ == '__main__':

    # List of all articles
    articles = os.listdir('../validArticles/')

    # List of test articles
    testArticles = os.listdir('../test/')

    # Setup multiprocessing
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)

    # Process valid articles
    summaries = pool.map(articleGensim, testArticles)
    print sum(summaries)
    print len(summaries)
    print float(sum(summaries))/len(summaries)