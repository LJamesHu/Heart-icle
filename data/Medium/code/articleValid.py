from bs4 import BeautifulSoup
import multiprocessing
import langdetect
import unidecode
import os


def article_validity(file):

    # If the file has been processed and was determined as valid, should already be in directory
    if os.path.exists('../validArticles/' + file):
        return

    # Open the article
    with open('../articles/' + file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Check if it has a top highlight
    highlight = soup.find('span', {'data-creator-ids': 'anon'})

    # If it does not have a highlight, go to the next article
    if not highlight:
        return


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


    # Check if it has a top highlight
    highlight = article.find('span', {'data-creator-ids': 'anon'})

    # If it does not have a highlight, go to the next article
    if not highlight:
        return

    # Clean up highlight and remove bad unicode
    highlightClean = unidecode.unidecode(" ".join(item.strip() for item in highlight.find_all(text=True)))

    # If highlight is not meaningfully long, go to the next article
    if len(highlightClean.split()) < 10:
        return


    # Get text information, clean up unicode
    articleClean = unidecode.unidecode(" ".join(item.strip() for item in article.find_all(text=True)))

    # Check if the article is meaningfully long
    if articleClean == None:
        return
    if len(articleClean.split()) < 300:
        return

    # Check if English article
    if langdetect.detect(articleClean) != 'en':
        return

    # Check if enough sentences
    if articleClean.count('.') < len(articleClean.split())/40:
        return

    # Move all valid articles
    with open('../validArticles/' + file, 'wb') as f2:
        f2.write(str(soup))

if __name__ == '__main__':

    # List of articles
    articles = os.listdir('../articles/')

    # Setup multiprocessing
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)

    # Process valid articles
    pool.map(article_validity, articles)