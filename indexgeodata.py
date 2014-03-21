import geohash
import json
from sklearn.feature_extraction.text import onlineTfidfVectorizer

def load_idf():
    global vectorizer
    f1 = open('idf.txt' , 'r')
    vectorizer.analyze2 = vectorizer.build_analyzer()
    vectorizer.vocabulary_ = json.loads(f1.readline())
    vectorizer.idf_ = json.loads(f1.readline())
    vectorizer.total_count = int(f1.readline())
    vectorizer.document_counts = json.loads(f1.readline())
    vectorizer.stop_words_ = set()
    f1.close()

f ='newyork.txt'
dic = {}
with open(f) as infile:
    for line in infile:
        line = json.loads(line)
        x = float(line['geo']['coordinates'][0])
        y = float(line['geo']['coordinates'][1])
        dic[geohash.encode(x,y,4)] = dic.setdefault( geohash.encode(x,y,4) , "")+" " + line['text']
l = dic.keys()

vectorizer = onlineTfidfVectorizer(min_df = 1, smooth_idf=True, stop_words='english')
load_idf()
terms = []
print l
print len(l)
cordinatesx = []
cordinatesy = []

for t in dic:
    terms.append(dic[t])
for t in l:
    cordinatesx.append(geohash.decode(t)[0])
    cordinatesy.append(geohash.decode(t)[1])
print cordinatesx
print cordinatesy
X = vectorizer.fit_transform(terms)
print X.get_shape()
X = X.toarray()
voc = vectorizer.vocabulary_
voc2 = voc.keys()
totalvoc = []
keywords = []
for i in range(len(terms)):
    voc2.sort(key = lambda x :-X[i][voc[x]])
    totalvoc.append(voc2[:5])
    keywords.append(voc2[0] + ' , ' + voc2[1] + ' , ' + voc2[2] + ' , ' + voc2[3] + ' , ' + voc2[4])
print keywords
print totalvoc

