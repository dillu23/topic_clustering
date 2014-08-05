from lshash import LSHash
#from rawTweets_parser import processfile
from text import onlineTfidfVectorizer
import json
import os
import numpy as np
import scipy.sparse as sp
import cProfile
import time


def write_clusters(i, cl, clusters, tweets_dump, fn, loc):
    f = open(loc + '/' + str(fn) + '/' + str(i) + '.txt', 'w')
    f2 = open(loc +'/current/' + str(i) + '.txt', 'w')
    for x in clusters[cl[i]]:
        f.write(json.dumps(tweets_dump[x]) + '\n')
        f2.write(json.dumps(tweets_dump[x]) + '\n')

def run():
    initial = True
    size = 200000
    tweet_ids = []
    tweet_text = []
    counter = 0
    num_hashtables = 4      ## recompute the random vectors if this is changed
    dimension = 5000000      ## recompute the random vectors if this is changed
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


    completed = open('/tmp/completed_tmp.txt')
    completed = completed.readlines()
    completed = set([x.replace('\n', '') for x in completed])

    while(True):
        clusters_size_prev = {}
        files = []
        for root, dirs, filenames in os.walk('/tmp/tweets_tmp/'):
            for fname in filenames:
                if fname != '.DS_Store':
                    files.append(fname)
        files = set(files)
        files = files - completed
        if len(files) == 0:
            print 'sleeping'
            time.sleep(3000)
            print 'checking'
            continue
        #print files
        tweets_dump = {}
        tweet_ids = []
        tweet_text = []
        time_sleep = time.time()
        for fn in files:
            print fn
            time_tmp2 = time.time()
            with open('/tmp/tweets_tmp/' + fn) as infile:
                for line in infile:
                    ## load 2000 tweets at a time 
                    
                    tweet = json.loads(line)
                    tweet_ids.append(tweet['id'])
                    tweet_text.append(tweet['filtered_text'])
                    tweets_dump[str(tweet['id'])] = tweet['text']

                    counter = counter + 1
                    t2 = 0
                    if counter%size == 0:
                        t1 = time.clock()

                        ## X contains te tf-idf score of the tweets in the "sparse row matrix" format
                        if initial:
                            X = vectorizer.fit_transform(tweet_text)
                        else:
                            X = vectorizer.transform(tweet_text)
                        #print X.get_shape()
                        #print len(vectorizer.vocabulary_)

                        ## if the total number of keywords exceed the pre-specified dimension, raise error
                        if X.get_shape()[0] > dimension:
                            print X.get_shape()
                            print "dimension exceeded"
                            raise
                        for i in range(X.get_shape()[0]):

                            temp_tweet = X.getrow(i)

                            ## query for the nearest neighbor from the lshash tables
                            nn = lsh.arpoxNN(temp_tweet, L=comparisons)
                            c = 2
                            scase = False

                            ## if nearesr neighbor is not null and the cosine similarity is less than the threshold, add the tweet to the respective cluster
                            cluster_id = -1
                            if nn is not None:
                                ((a, (b,d)),c) = nn
                                if c <= cos_threshold:
                                    cluster_id = d
                                    clusters.setdefault(d,[]).append(tweet_ids[i])
                                #else:
                                #    scase = True

                            ## else, linearly search through the previous 2000 + i tweets to find the nearest neighbor
                            """ code to linearly search through the tweets"""
                            if (c > cos_threshold or nn is None or scase):
                                cluster_id = num_clusters
                                clusters.setdefault(num_clusters, []).append(tweet_ids[i])
                                num_clusters = num_clusters + 1

                            ### index the tweet into the hsh tables
                            lsh.index(input_point = temp_tweet, extra_data = tuple([tweet_ids[i], cluster_id]))
                        initial = False
 
                        tweet_ids = []
                        tweet_text = []
                        #print counter
                        #print time.clock() - t1
                        f2 = open('time.txt','a')
                        f2.write(str(time.clock()-t1) + '\n')
                        f2.close()
                        """
                        if counter%100000==0:
                            f2 = open('result.txt', 'w')
                            f2.write(json.dumps(clusters) + "\n")
                            f3 = open('vocab.txt', 'w')
                            f4 = open('vectorizer.txt', 'w')
                            f3.write(json.dumps(vectorizer.vocabulary_) + "\n")
                            f4.write(json.dumps(vectorizer.idf_) + "\n")
                            #print clusters
                            #print vectorizer.vocabulary_
                            f2.close()
                            f3.close()
                            f4.close()
                        """
            print 'done'
            print counter
            print str(time.time() - time_tmp2)
            f = open('/tmp/completed_tmp.txt', 'a')
            f.write(fn + '\n')
            f.close()
            completed.add(fn)
        print "all done"
        time_temp = time.time()
        if not os.path.exists('/home/y/share/htdocs/clusters/' + str(time_temp)):
            os.makedirs('/home/y/share/htdocs/clusters/' + str(time_temp))
        if not os.path.exists('/home/y/share/htdocs/clusters/current'):
            os.makedirs('/home/y/share/htdocs/clusters/current')
        
        clusters_size = {}

        for x in clusters:
            clusters_size[x] = len(clusters[x])
        f = open('/home/y/share/htdocs/clusters/' + str(time_temp) + '/sizes.txt', 'w')
        f.write(json.dumps(clusters_size))
        f.close()
        f = open('/home/y/share/htdocs/clusters/current/sizes.txt', 'w')
        f.write(json.dumps(clusters_size))
        f.close()
        cls = clusters_size.keys()
        cls.sort(key = lambda x : -1 * clusters_size[x])
        cl = []
        for x in cls:
            if clusters_size[x] >=10:
                cl.append(x)
        arr = []
        for i in range(len(cl)):
            write_clusters(i, cl, clusters, tweets_dump, time_temp, '/home/y/share/htdocs/clusters')
            arr.append(cl[i])
        f = open('/home/y/share/htdocs/clusters/' + str(time_temp) + '/list.txt', 'w')
        f.write(json.dumps(arr))
        f.close()
        f = open('/home/y/share/htdocs/clusters/current/list.txt', 'w')
        f.write(json.dumps(arr))
        f.close()
        f = open('/home/y/share/htdocs/clusters/list.txt', 'a')
        f.write(str(time_temp) + '\n')
        f.close()

        if not os.path.exists('/home/y/share/htdocs/ratio_clusters/' + str(time_temp)):
            os.makedirs('/home/y/share/htdocs/ratio_clusters/' + str(time_temp))
        if not os.path.exists('/home/y/share/htdocs/ratio_clusters/current'):
            os.makedirs('/home/y/share/htdocs/ratio_clusters/current')

        ratio = {}
        for x in clusters_size:
            if clusters_size[x]>=10:
                r = 1
                if (x in clusters_size_prev and clusters_size_prev[x] != 0):
                        r = clusters_size_prev[x]
                ratio[x] = clusters_size[x]*1.0/r
        ratio_keys = ratio.keys()
        ratio_keys.sort(key = lambda x : -1 * ratio[x])
        ratio_keys = ratio_keys[:300]
        arr = []
        for i in range(len(ratio_keys)):
            write_clusters(i, ratio_keys, clusters, tweets_dump, time_temp, '/home/y/share/htdocs/ratio_clusters')
            arr.append(ratio_keys[i])
        f = open('/home/y/share/htdocs/ratio_clusters/' + str(time_temp) + '/list.txt', 'w')
        f.write(json.dumps(arr))
        f.close()
        f = open('/home/y/share/htdocs/ratio_clusters/current/list.txt', 'w')
        f.write(json.dumps(arr))
        f.close()
        f = open('/home/y/share/htdocs/ratio_clusters/list.txt', 'a')
        f.write(str(time_temp) + '\n')
        f.close()

        clusters_size_prev = {}
        for x in clusters_size:
            clusters_size_prev[x] = clusters_size[x]

        clusters = {}
        time.sleep(max(0, 3600 - (time.time() - time_sleep)))
        
        

run()
#cProfile.run('run()')
