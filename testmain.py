from lshash import LSHash
#from rawTweets_parser import processfile
from text import onlineTfidfVectorizer
import json
import os
import numpy as np
import scipy.sparse as sp
import cProfile
import time

def run():
    initial = True
    error_string = ""
    size = 200000
    tweet_ids = []
    tweet_text = []
    counter = 0
    num_hashtables = 13      ## recompute the random vectors if this is changed
    dimension = 500000       ## recompute the random vectors if this is changed
    hash_size = 13          ## length of the LSHash of the tweets
    bucket_size = 100       ## size of the queue for each hash in the hash tables
    comparisons = 50       ## upper bound on the number of comparisons (dot product) to find the nearest neighbor
    cos_threshold = .7      ## threshold for the similarity of two tweets

    ## initialize the tf-idf vectorizer
    vectorizer = onlineTfidfVectorizer(min_df = 1, smooth_idf=True, stop_words='english', min_dict_size = dimension)
    ## initialize the hash tables, specify the hash size, number of hash tabeles and the queue size
    lsh = LSHash(hash_size = hash_size, input_dim = dimension, num_hashtables=num_hashtables, max_queue_size= bucket_size)


    clusters = {}           ## maintain the clusters
    num_clusters = 0
    inv_index = {}          ## inverse mapping from tweet_id to clusters
    Y = None
    Y1 = None
    f_d = open("output.txt",'w')
    loc = "tweets/"
    for root, dirs, filenames in os.walk(loc):
        for f in filenames:
            with open(loc+f) as infile:
                for line in infile:

                    ## load 2000 tweets at a time 
                    #print f
                    tweet = json.loads(line)
                    tweet_ids.append(tweet['id'])
                    tweet_text.append(tweet['text'])
                    counter = counter + 1
                    t2 = 0
                    if counter%10000==0:
                        print counter
                    if counter%size == 0:
                        t1 = time.clock()
                        ## X contains te tf-idf score of the tweets in the "sparse row matrix" format
                        if initial:
                            X = vectorizer.fit_transform(tweet_text)
                        else:
                            X = vectorizer.transform(tweet_text)
                        print X.get_shape()
                        print len(vectorizer.vocabulary_)

                        ## if the total number of keywords exceed the pre-specified dimension, raise error
                        if X.get_shape()[0] > dimension:
                            print X.get_shape()
                            print "dimension exceeded"
                            raise
                        for i in range(X.get_shape()[0]):
                            temp_tweet = X.getrow(i)
                            if i%200 == 0:
                                print str(time.clock() - t1)
                                t1 = time.clock()
                            ## query for the nearest neighbor from the lshash tables
                            #nn = lsh.arpoxNN(temp_tweet, L=comparisons)
                            nn = None
                            c = 2
                            scase = False

                            ## if nearesr neighbor is not null and the cosine similarity is less than the threshold, add the tweet to the respective cluster

                            if nn is not None:
                                ((a, b),c) = nn
                                if c <= cos_threshold:
                                    inv_index[tweet_ids[i]] = inv_index[b]
                                    clusters.setdefault(inv_index[b],[]).append(tweet_ids[i])
                                    error_string = error_string + "0"
                                #else:
                                #    scase = True

                            ## else, linearly search through the previous 2000 + i tweets to find the nearest neighbor
                            """ code to linearly search through the tweets"""
                            if (c > cos_threshold or nn is None or scase):
                                searchY = False

                                if (i==0 and not initial):
                                    searchY = True
                                if (i==0 and initial):
                                    inv_index[tweet_ids[i]] = num_clusters
                                    clusters.setdefault(num_clusters, []).append(tweet_ids[i])
                                    error_string = error_string + "1"
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
                                            error_string = error_string + "1"
                                    else:
                                        inv_index[tweet_ids[i]] = inv_index[t3]
                                        clusters.setdefault(inv_index[t3], []).append(tweet_ids[i])
                                        error_string = error_string + "0"
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
                                        clusters.setdefault(inv_index[tweet_ids[i]], []).append(tweet_ids[i])
                                        error_string = error_string + "0"

                                    else:
                                        inv_index[tweet_ids[i]] = num_clusters
                                        clusters.setdefault(num_clusters, []).append(tweet_ids[i])
                                        num_clusters = num_clusters + 1
                                        error_string = error_string + "1"

                            ### index the tweet into the hsh tables
                            #lsh.index(input_point = temp_tweet, extra_data = tweet_ids[i])
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
                        if counter%10000==0:
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

    f2 = open('result.txt', 'w')
    f2.write(json.dumps(clusters) + "\n")
    f3 = open('vocab.txt', 'w')
    f4 = open('vectorizer.txt', 'w')
    f5 = open('inv_index.txt', 'w')
    f3.write(json.dumps(vectorizer.vocabulary_) + "\n")
    f4.write(json.dumps(vectorizer.idf_) + "\n")
    f5.write(json.dumps(inv_index))
    #print clusters
    #print vectorizer.vocabulary_
    f2.close()
    f3.close()
    f4.close()
    f5.close()
    f2 = open('error_string.txt', 'w')
    f2.write(error_string)
    f2.close()

run()
#cProfile.run('run()')
