import cPickle as pickle

with open('../dfArticles.pkl') as pkl:
    dfArticles = pickle.load(pkl)

with open('../articles.txt', 'wb') as articles:
    articles.write('\n'.join(dfArticles['article']))
    articles.write('\n')

with open('../highlights.txt', 'wb') as highlights:
    highlights.write('\n'.join(dfArticles['highlight']))
    highlights.write('\n')