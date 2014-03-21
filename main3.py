from lshash import LSHash
#from rawTweets_parser import processfile
from text import onlineTfidfVectorizer
import json
import os
import numpy as np
import scipy.sparse as sp
import cProfile
import time
def dotproduct(x,y):
    p = 0
    a = set(x.indices).intersection(set(y.indices))
    for i in a:
        p += x.data[np.where(x.indices == i)[0][0]]*y.data[np.where(y.indices == i)[0][0]]*1.0
    return p
        
def cosine_dist(x,y):
    return 1 - float(dotproduct(x,y))/((dotproduct(x,x) + dotproduct(y,y))**.5)
def run():
    initial = True
    size = 2000
    tweet_ids = []
    tweet_text = []
    counter = 0
    num_hashtables = 1 ## recompute the random vectors if this is changed
    dimension = 500000  ## recompute the random vectors if this is changed
    hash_size = 13
    bucket_size = 100
    comparisons = 200
    cos_threshold = .5
    vectorizer = onlineTfidfVectorizer(min_df = 1, smooth_idf=True, stop_words='english', min_dict_size = dimension)
    lsh = LSHash(hash_size = hash_size, input_dim = dimension, num_hashtables=num_hashtables, max_queue_size= bucket_size)
    clusters = {}
    num_clusters = 0
    inv_index = {}
    Y = None
    Y1 = None
    f_d = open("output.txt",'w')
    loc = "processed_tweets/"
    for root, dirs, filenames in os.walk(loc):
        for f in filenames:
            with open(loc+f) as infile:
                for line in infile:
                    tweet = json.loads(line)
                    tweet_ids.append(tweet['id'])
                    tweet_text.append(tweet['text'])
                    counter = counter + 1
                    t2 = 0
                    if counter%size == 0:
                        t1 = time.clock()
                        if initial:
                            X = vectorizer.fit_transform(tweet_text)
                        else:
                            X = vectorizer.transform(tweet_text)
                        print X.get_shape()
                        print len(vectorizer.vocabulary_)
                        if X.get_shape()[0] > dimension:
                            print X.get_shape()
                            print "err"
                            raise
                        for i in range(X.get_shape()[0]):
                            temp_tweet = X.getrow(i)
                            nn = lsh.arpoxNN(temp_tweet, L=comparisons)
                            c = 2
                            scase = False
                            if nn is not None:
                                ((a, b),c) = nn
                                if c <= cos_threshold:
                                    inv_index[tweet_ids[i]] = inv_index[b]
                                    clusters.setdefault(inv_index[b],[]).append(tweet_ids[i])
                                #else:
                                #    scase = True
                            if (c > cos_threshold or nn is None or scase):
                                inv_index[tweet_ids[i]] = num_clusters
                                clusters.setdefault(num_clusters, []).append(tweet_ids[i])
                                num_clusters = num_clusters + 1
                            lsh.index(input_point = temp_tweet, extra_data = tweet_ids[i])
                        initial = False
                        Y = X
                        Y1 = tweet_ids[:]
                        tweet_ids = []
                        tweet_text = []
                        print counter
                        print time.clock() - t1
                        f2 = open('time.txt','a')
                        f2.write(str(time.clock()-t1) + '\n')
                        f2.close()
                        if counter%100000==0:
                            f2 = open('result.txt', 'a')
                            f2.write(json.dumps(clusters) + "\n")
                            f3 = open('vocab.txt', 'a')
                            f4 = open('vectorizer.txt', 'a')
                            f3.write(json.dumps(vectorizer.vocabulary_) + "\n")
                            f4.write(json.dumps(vectorizer.idf_) + "\n")
                            #print clusters
                            #print vectorizer.vocabulary_
                            f2.close()
                            f3.close()
                            f4.close()
#run()
cProfile.run('run()')

