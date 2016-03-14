from selenium import webdriver
import time
import os

# Setup selenium
driver = webdriver.Firefox()

# Open list of articles that need to be scraped
with open('articleList.txt') as f:
    articles = f.read().split()

# Iterate
for article in articles:

    # Check if already scraped with file existing
    if os.path.exists('articles/' + article.split('/')[-1] + '.html'):
        continue

    # Open article
    print article
    driver.get(article)

    # Sleep to allow javascript, ajax calls etc. to load completely on the page
    time.sleep(5)

    # Scroll to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Write
    with open('articles/' + article.split('/')[-1] + '.html', 'wb') as f:
        f.write(driver.page_source.encode('utf-8'))

# Intentionally outside so doesn't have to reload Selenium each iteration
driver.close()