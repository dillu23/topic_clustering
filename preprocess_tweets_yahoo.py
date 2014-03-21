"""
import os
import json
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
				tweet_id = tweet_id + 1
				c['text'] = b
				f2.write(json.dumps(c) + '\n')
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


