import json
import os
from text import onlineTfidfVectorizer

f = open('results/vectorizer.txt')
a = f.readline()
while(a):
	b = a
	a = f.readline()

idf = json.loads(b)
dimension = 500000
for dirs, root, files in os.walk('clusters2/'):
	for fname in files:
		tfidf = {}
		f = open('clusters2/'+fname)
		f2 = open('cluster_topic/' + fname, 'w')
		a = f.readlines()
		vectorizer = onlineTfidfVectorizer(min_df = 1, smooth_idf=True, stop_words='english', min_dict_size = dimension)
		b = vectorizer.fit_transform(a)
		tf = vectorizer.document_counts
		for x in tf:
			if x in idf:
				tfidf[x] = tf[x] * idf[x]
		tfkeys = tfidf.keys()
		tfkeys.sort(key = lambda x : -1* tfidf[x])
		s = ""
		for x in tfkeys:
			s = s + " " + x
		f2.write(s)
		f2.close()

