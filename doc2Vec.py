from collections import namedtuple
from gensim.models import Doc2Vec
import gensim.models.doc2vec
from random import shuffle
import multiprocessing
import pandas as pd
import time

# Setup for Doc2Vec
SentimentDocument = namedtuple('SentimentDocument', 'words tags')

cores = multiprocessing.cpu_count()
assert gensim.models.doc2vec.FAST_VERSION > -1

# Prepare data for Doc2Vec
alldocs = []
df = pd.read_csv('alldocs.txt', sep='sepsepsepsep', names=['tags', 'words'], engine='python')

df.apply(lambda x: alldocs.append(SentimentDocument(x['words'].split(), [x['tags']])), axis=1)

doc_list = alldocs[:]

# Setup model
d2v = Doc2Vec(dm=1, dm_mean=1, size=200, window=10, negative=5, hs=0, min_count=5, workers=cores)

d2v.build_vocab(alldocs)

# Set parameters
alpha, min_alpha, passes = (0.025, 0.001, 20)
alpha_delta = (alpha - min_alpha) / passes
print 'Started at %s' % time.ctime()

# Run through epochs
for epoch in range(passes):
    shuffle(doc_list)
    d2v.alpha, d2v.min_alpha = alpha, alpha
    d2v.train(doc_list)

    print('Completed pass %i at alpha %f at %s' % (epoch + 1, alpha, time.ctime()))
    alpha -= alpha_delta

# Save final model
d2v.save('d2v.model')
