
import os
import json
from starbase import Connection

c = Connection(host = '127.0.0.1', port = 8080)
t = c.table('tweets_test')
tweet_id = 1
loc = 'tweets/'
loc2 = 'processed_tweets/'
for root, dirs, filename in os.walk(loc):
	for fname in filename:
		f2 = open(loc2 + fname, 'w')
		with open(loc + fname) as infile:
			for line in infile:
				b = line[line.index('\t')+1:]
				c = {}
				c['id'] = tweet_id
				c['text'] = b
				t.insert(str(tweet_id), {'cf': {'text': b}})
				f2.write(json.dumps(c) + '\n')
				tweet_id = tweet_id + 1
		f2.close()


"""
import os
import json
tweet_id = 1
loc = 'processed_tweets/'
loc2 = 'tweets_id_data.txt'
upper = {}
lower = {}
for root, dirs, filename in os.walk(loc):
	for fname in filename:
		f = open(loc + fname)
		a = f.readlines()
		b = json.loads(a[0])
		c = json.loads(a[len(a)-1])
		lower[int(c['id'])] = fname
		upper[int(b['id'])] = fname
		f.close()

f = open(loc2, 'w')
f.write(json.dumps(lower))
f.write('\n')
f.write(json.dumps(upper))
f.close()
"""

