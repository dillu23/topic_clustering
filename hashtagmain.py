from lshash import LSHash
import os
#from rawTweets_parser import processfile
from sklearn.feature_extraction.text import onlineTfidfVectorizer
import json
import numpy as np
import scipy.sparse as sp
import cProfile
import time
initial = True
size = 2000
tweet_ids = []
tweet_text = []
tweet_hashtags = []
counter = 0
num_hashtables = 5 ## recompute the random vectors if this is changed
dimension = 100000  ## recompute the random vectors if this is changed
hash_size = 13
bucket_size = 100
comparisons = 300
cos_threshold = .5

lsh = LSHash(hash_size = hash_size, input_dim = dimension, num_hashtables=num_hashtables, matrices_filename="random_vectors-100000,5.npz", max_queue_size= bucket_size)
clusters = {}
num_clusters = 0
inv_index = {}
Y = None
Y1 = None
HY = None
HY1 = None
saveDict = False 
parentdirectory = '2012/07/'
subdirectories1 = ['0' + str(x) + '/' for x in range(1,10)] + [str(x) + '/' for x in range(10,32)]
subdirectories2 = ['0' + str(x) + '/' for x in range(10)] + [str(x) + '/' for x in range(10,24)]
def dotproduct(x,y):
    p = 0
    a = set(x.indices).intersection(set(y.indices))
    for i in a:
        p += x.data[np.where(x.indices == i)[0][0]]*y.data[np.where(y.indices == i)[0][0]]*1.0
    return p
        
def cosine_dist(x,y):
    return 1 - float(dotproduct(x,y))/((dotproduct(x,x) + dotproduct(y,y))**.5)

def processclusters(f, path):
    global initial
    global size
    global tweet_ids
    global tweet_text
    global tweet_hashtags
    global counter
    global num_hashtables ## recompute the random vectors if this is changed
    global dimension  ## recompute the random vectors if this is changed
    global hash_size
    global bucket_size
    global comparisons
    global cos_threshold
    global vectorizer
    global hashtagvectorizer
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
                st = ""
                for i in tweet['entities']['hashtags']:
                    st = st + " " + i['text']
                tweet_hashtags.append(st)
            except:
                print "json line error"
        t2 = 0
        t1 = time.clock()
        if not saveDict:
            X = vectorizer.fit_transform(tweet_text)
            X1 = hashtagvectorizer.fit_transform(tweet_hashtags)
        else:
            X = vectorizer.transform(tweet_text)
            X1 = hashtagvectorizer.transform(tweet_hashtags)
        print X.get_shape()
        print X1.get_shape()
        print len(vectorizer.vocabulary_)
        print len(hashtagvectorizer.vocabulary_)
        if X.get_shape()[0] > dimension or X1.get_shape()[0] > dimension:
            print X.get_shape()
            print X1.get_shape()
            print "err"
            raise
        for i in range(X.get_shape()[0]):
            temp_tweet = X.getrow(i)
            temp_hashtag = X1.getrow(i)
            nn = lsh.arpoxNN_2((temp_tweet, temp_hashtag), L=comparisons)
            c = 2
            scase = False
            if nn is not None:
                ((a, b),c) = nn
                b = b[1]
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
                    Z1 = X1[:i]
                    #print temp_tweet.shape
                    t2 = temp_tweet.transpose()
                    ht2 = temp_hashtag.transpose()
                    #print i
                    a1 = Z.dot(t2).toarray()
                    ha1 = Z1.dot(ht2).toarray()
                    a2 = Z.multiply(Z).sum(axis = 1)
                    ha2 = Z1.multiply(Z1).sum(axis = 1)
                    a3 = sp.csr_matrix(t2.multiply(t2).sum()).toarray()
                    ha3 = sp.csr_matrix(ht2.multiply(ht2).sum()).toarray()
                    a2 = sp.csc_matrix(a2).toarray()
                    ha2 = sp.csc_matrix(ha2).toarray()
                    b = [j for j in range(Z.shape[0])]
                
                    a = min(b, key = lambda x: 1-(float(a1[x][0])/((a2[x][0] + a3[0][0])**.5) + float(ha1[x][0])/((ha2[x][0] + ha3[0][0])**.5))/2)
                    #a = min(Z, key = lambda x: cosine_dist(x[0], temp_tweet))
                    #print a
                    t3 = tweet_ids[a]
                    if (1-(float(a1[a][0])/((a2[a][0] + a3[0][0])**.5) + float(ha1[a][0])/((ha2[a][0] + ha3[0][0])**.5))/2)> cos_threshold:
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
                    Z1 = HY
                    t2 = temp_tweet.transpose()
                    #print i
                    a1 = Z.dot(t2).toarray()
                    ha1 = Z1.dot(ht2).toarray()
                    a2 = Z.multiply(Z).sum(axis = 1)
                    h2 = Z1.multiply(Z1).sum(axis = 1)
                    a3 = sp.csr_matrix(t2.multiply(t2).sum()).toarray()
                    ha3 = sp.csr_matrix(ht2.multiply(ht2).sum()).toarray()
                    a2 = sp.csc_matrix(a2).toarray()
                    ha2 = sp.csc_matrix(ha2).toarray()
                    b1 = [j for j in range(Z.shape[0])]
                    a = min(b1, key = lambda x: 1-(float(a1[x][0])/((a2[x][0] + a3[0][0])**.5) + float(ha1[x][0])/((ha2[x][0] + ha3[0][0])**.5))/2)
                    t3 = Y1[a]
                    if (1-(float(a1[a][0])/((a2[a][0] + a3[0][0])**.5) + float(ha1[a][0])/((ha2[a][0] + ha3[0][0])**.5))/2)< cos_threshold:
                        inv_index[tweet_ids[i]] = inv_index[t3]
                    else:
                        inv_index[tweet_ids[i]] = num_clusters
                        clusters.setdefault(num_clusters, []).append(tweet_ids[i])
                        num_clusters = num_clusters + 1
            lsh.index(input_point = temp_tweet, extra_data = (temp_hashtag, tweet_ids[i]))
    initial = True
    saveDict = True
    Y = X
    Y1 = tweet_ids[:]
    HY = X1
    tweet_ids = []
    tweet_text = []
    tweet_hashtags = []
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
    global hashtagvectorizer
    global lsh
    global clusters
    global num_clusters
    global inv_index
    global Y
    global Y1
    vectorizer =  onlineTfidfVectorizer(min_df = 1, smooth_idf=True, stop_words='english', min_dict_size = dimension)
    hashtagvectorizer = onlineTfidfVectorizer(min_df = 1, smooth_idf=True, stop_words='english', min_dict_size = dimension)
    parentdirectory = 'twitterlogs/markedData/totalData/2012/07/'
    subdirectories1 = ['0' + str(x) + '/' for x in range(4,7)] + [str(x) + '/' for x in range(10,0)]
    subdirectories2 = ['0' + str(x) + '/' for x in range(10)] + [str(x) + '/' for x in range(10,24)]
    for i in subdirectories1:
        for j in subdirectories2:
            path = parentdirectory + i + j
            for root, dirs, filename in os.walk(path):
                for f in filename:
                    if (f != 'log.txt' and f!= '.DS_Store'):
                        print f
                        processclusters(f, path)
                log = open("idf.txt", 'w')
                log2 = open("idf_hash.txt", 'w')
                log.write(json.dumps(vectorizer.vocabulary_) + "\n")
                log2.write(json.dumps(hashtagvectorizer.vocabulary_) + "\n")
                log.write(json.dumps(vectorizer.idf_) + "\n")
                log2.write(json.dumps(hashtagvectorizer.idf_) + "\n")
                log.write(str(vectorizer.total_count) + "\n")
                log2.write(str(hashtagvectorizer.total_count) + "\n")
                log.write(json.dumps(vectorizer.document_counts) + "\n")
                log2.write(json.dumps(hashtagvectorizer.document_counts) + "\n")
                log.write(json.dumps(clusters) + "\n")
                log.close()
                log2.close()
    f2 = open('result.txt', 'a')
    f2.write(json.dumps(clusters))
    f2.write(json.dumps(vectorizer.vocabulary_))
    f2.write(json.dumps(vectorizer.idf_))
    print clusters
    print vectorizer.vocabulary_
    f2.close()
run()
#if '__name__' == '__main__':
#cProfile.run('run()')
