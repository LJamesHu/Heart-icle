from sklearn.cross_validation import train_test_split
from shutil import copyfile
import os

articles = os.listdir('../validArticles/')

trainArticles, testArticles = train_test_split(articles, test_size=0.2, random_state=42)

for article in trainArticles:
    copyfile('../validArticles/' + article, '../train/' + article)

for article in testArticles:
    copyfile('../validArticles/' + article, '../test/' + article)