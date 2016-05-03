from bs4 import BeautifulSoup, Comment
import unidecode
import os
import re


# List all files in the directory to travel down
articles = os.listdir('../articles/')

with open('../articles.txt', 'wb') as af:

    for file in articles:

        # Open file
        with open('articles/' + file, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        article = soup.find('div', {'class': 'article-body'})

        # Remove small text
        [x.extract() for x in article.find_all('small')]

        # Remove asides (quotations from article)
        [x.extract() for x in article.find_all('aside')]

        # Remove picture captions
        [x.extract() for x in article.find_all('figcaption')]

        # Remove certain charts
        [x.extract() for x in article.find_all('iframe')]

        # Remove comments
        [x.extract() for x in article.findAll(text=lambda text:isinstance(text, Comment))]

        # Get text from article
        articleClean = unidecode.unidecode(" ".join(item.strip() for item in article.find_all(text=True)))

        # Check if the article is meaningfully long
        try:
            if len(articleClean.split()) < 100:
                continue
        except:
            continue

        # Normalize text as per original Doc2Vec spec
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
        articleClean = re.sub('\n', '', articleClean)

        # Write to file
        af.write(articleClean.strip() + '\n')