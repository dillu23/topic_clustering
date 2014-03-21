from lshash import LSHash
from sklearn.feature_extraction.text import onlineTfidfVectorizer
import cProfile
import json
import numpy as np
import os
import scipy.sparse as sp
import time
#from rawTweets_parser import processfile
initial = True
size = 2000
tweet_ids = []
tweet_text = []
counter = 0
num_hashtables = 5 ## recompute the random vectors if this is changed
dimension = 100000  ## recompute the random vectors if this is changed
hash_size = 13
bucket_size = 1000
comparisons = 3000
cos_threshold = .7

lsh = LSHash(hash_size = hash_size, input_dim = dimension, num_hashtables=num_hashtables, matrices_filename="randomvectors.npz", max_queue_size= bucket_size)
clusters = {}
num_clusters = 0
inv_index = {}
Y = None
Y1 = None
saveDict = False

def load_idf():
    global vectorizer
    global initial
    global saveDict
    saveDict = True
    f1 = open('idf.txt' , 'r')
    vectorizer.analyze2 = vectorizer.build_analyzer()
    vectorizer.vocabulary_ = json.loads(f1.readline())
    vectorizer.idf_ = json.loads(f1.readline())
    vectorizer.total_count = int(f1.readline())
    vectorizer.document_counts = json.loads(f1.readline())
    vectorizer.stop_words_ = set()
    f1.close()
def processclusters(f, path):
    global initial
    global size
    global tweet_ids
    global tweet_text
    global counter
    global num_hashtables ## recompute the random vectors if this is changed
    global dimension  ## recompute the random vectors if this is changed
    global hash_size
    global bucket_size
    global comparisons
    global cos_threshold
    global vectorizer
    global lsh
    global clusters
    global num_clusters
    global inv_index
    global Y
    global Y1
    global saveDict
    with open(path + f) as infile:
        for line in infile:
            try:
                tweet = json.loads(line)
                tweet_ids.append(tweet['id'])
                tweet_text.append(tweet['text'])
            except:
                print "json line error"
        t2 = 0
        t1 = time.clock()
        if not saveDict:
            X = vectorizer.fit_transform(tweet_text)
        else:
            X = vectorizer.transform(tweet_text)
        print X.get_shape()
        print len(vectorizer.vocabulary_)
        if X.get_shape()[0] > dimension:
            print X.get_shape()
            print "err"
            raise
        xcounter = 0
        for i in range(X.get_shape()[0]):
            temp_tweet = X.getrow(i)
            nn = lsh.arpoxNN(temp_tweet, L=comparisons)
            #nn = None
            c = 2
            scase = False
            if nn is not None:
                xcounter += 1
                ((a, b),c) = nn
                if c <= cos_threshold:
                    inv_index[tweet_ids[i]] = inv_index[b]
                    clusters.setdefault(inv_index[b],[]).append(tweet_ids[i])
                #else:
                #    scase = True
            """
            if (c > cos_threshold or nn is None or scase):
                inv_index[tweet_ids[i]] = num_clusters
                clusters.setdefault(num_clusters, []).append(tweet_ids[i])
                num_clusters = num_clusters + 1
                
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
                
                    a = min(b, key = lambda x: 1-float(a1[x][0])/((a2[x][0] * a3[0][0])**.5))
                    #a = min(Z, key = lambda x: cosine_dist(x[0], temp_tweet))
                    #print a
                    t3 = tweet_ids[a]
                    if (1-float(a1[a][0])/((a2[a][0] * a3[0][0])**.5))> cos_threshold:
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
                    Z = Y
                    t2 = temp_tweet.transpose()
                    #print i
                    a1 = Z.dot(t2).toarray()
                    a2 = Z.multiply(Z).sum(axis = 1)
                    a3 = sp.csr_matrix(t2.multiply(t2).sum()).toarray()
                    a2 = sp.csc_matrix(a2).toarray()
                    b1 = [j for j in range(Z.shape[0])]
                    a = min(b1, key = lambda x: 1-float(a1[x][0])/((a2[x][0] * a3[0][0])**.5))
                    t3 = Y1[a]
                    if (1-float(a1[a][0])/((a2[a][0] * a3[0][0])**.5))< cos_threshold:
                        inv_index[tweet_ids[i]] = inv_index[t3]
                    else:
                        inv_index[tweet_ids[i]] = num_clusters
                        clusters.setdefault(num_clusters, []).append(tweet_ids[i])
                        num_clusters = num_clusters + 1 
                """
            lsh.index(input_point = temp_tweet, extra_data = tweet_ids[i])
    initial = True
    saveDict = True
    print xcounter
    Y = X
    Y1 = tweet_ids[:]
    tweet_ids = []
    tweet_text = []
    print time.clock() - t1
def run():
    global initial
    global size
    global tweet_ids
    global tweet_text
    global counter
    global num_hashtables ## recompute the random vectors if this is changed
    global dimension  ## recompute the random vectors if this is changed
    global hash_size
    global bucket_size
    global comparisons
    global cos_threshold
    global vectorizer
    global lsh
    global clusters
    global num_clusters
    global inv_index
    global Y
    global Y1
    initial = True
    vectorizer =  onlineTfidfVectorizer(min_df = 1, smooth_idf=True, stop_words='english', min_dict_size = dimension)
    load_idf()
    processclusters('testset.txt','')
    #print vectorizer.vocabulary_
    #print clusters
    #print inv_index
    fw = open('clusters.txt' , 'w')
    fw.write(json.dumps(clusters) + '\n')
    fw.write(json.dumps(inv_index) + '\n')
    fw.write(json.dumps(vectorizer.vocabulary_) + '\n')
    fw.write(json.dumps(vectorizer.idf_) + '\n')
run()
#cProfile.run('run()')
