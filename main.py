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
#    if len(x.data) == 0 or len(y.data) == 0:
#        return 1
#
#    a = x.dot(y.transpose()).data
#    
#    if len(a) == 0:
#        return 1
#    
#    b = x.dot(x.transpose()).data
#   c = y.dot(y.transpose()).data
    
#    return 1 - (float(a[0])) / ((b[0] + c[0]) ** .5)
    #try:
    #    return 1 - float(x.dot(y.transpose()).data[0])/((x.dot(x.transpose()).data[0] + y.dot(y.transpose()).data[0])**.5)
    #except:
        #return 1
#indir ='logs/'
#newdir = 'logs/processed/'
#processed_file = 'processedTweets.txt'
#for root, dirs, filenames in os.walk(indir):
#    for f in filenames:
#        if (f != '.DS_Store'):
#            try:
#                processfile(indir + f, processed_file)
#                #os.rename(indir +f,newdir +f)
#            except:
#                print f
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
                                searchY = False
                                if (i==0 and not initial):
                                    searchY = True
                                if (i==0 and initial):
                                    inv_index[tweet_ids[i]] = num_clusters
                                    clusters.setdefault(num_clusters, []).append(tweet_ids[i])
                                    num_clusters = num_clusters + 1
                                if (i!=0):
                                    Z = X[:i]
                                    #print temp_tweet.shape
                                    t2 = temp_tweet.transpose()
                                    #print i
                                    a1 = Z.dot(t2).toarray()
                                    a2 = Z.multiply(Z).sum(axis = 1)
                                    a3 = sp.csr_matrix(t2.multiply(t2).sum()).toarray()
                                    a2 = sp.csc_matrix(a2).toarray()
                                    b = [j for j in range(Z.shape[0])]
                                
                                    a = min(b, key = lambda x: 1-float(a1[x][0])/((a2[x][0] + a3[0][0])**.5))
                                    #a = min(Z, key = lambda x: cosine_dist(x[0], temp_tweet))
                                    #print a
                                    t3 = tweet_ids[a]
                                    if (1-float(a1[a][0])/((a2[a][0] + a3[0][0])**.5))> cos_threshold:
                                        if not initial and i != size-1:
                                            searchY = True
                                        else:
                                            inv_index[tweet_ids[i]] = num_clusters
                                            clusters.setdefault(num_clusters, []).append(tweet_ids[i])
                                            num_clusters = num_clusters + 1
                                    else:
                                        inv_index[tweet_ids[i]] = inv_index[t3]
                                        clusters.setdefault(inv_index[t3], []).append(tweet_ids[i])
                                if searchY == True:
                                    Z = Y[i:]
                                    t2 = temp_tweet.transpose()
                                    #print i
                                    a1 = Z.dot(t2).toarray()
                                    a2 = Z.multiply(Z).sum(axis = 1)
                                    a3 = sp.csr_matrix(t2.multiply(t2).sum()).toarray()
                                    a2 = sp.csc_matrix(a2).toarray()
                                    b1 = [j for j in range(Z.shape[0])]
                                    a = min(b1, key = lambda x: 1-float(a1[x][0])/((a2[x][0] + a3[0][0])**.5))
                                    t3 = Y1[a + i]
                                    if (1-float(a1[a][0])/((a2[a][0] + a3[0][0])**.5))< cos_threshold:
                                        inv_index[tweet_ids[i]] = inv_index[t3]
                                    else:
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

