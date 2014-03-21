import csv
import json
textdata = {}
with open('testset.txt') as infile:
    for line in infile:
        tweet = json.loads(line)
        textdata[int(tweet['id'])] = tweet['text']

a1 = {}
a2 = {}
a3 = {}
a4 = {}
a5 = {}

f = open('heirarchichal_clustering2.csv' , 'r')
f2 = open('h_clusters.txt')
cs = csv.reader(f)
for line in cs:
    x = [int(t) for t in f2.readline().strip().split()]
    a1.setdefault(int(x[0]), []).append(int(line[0]))
    a2.setdefault(int(x[1]), []).append(int(line[0]))
    a3.setdefault(int(x[2]), []).append(int(line[0]))
    a4.setdefault(int(x[3]), []).append(int(line[0]))
    a5.setdefault(int(x[4]), []).append(int(line[0]))
f.close()
f2.close()

for x in a1:
    tdata = []
    for i in a1[x]:
        tdata.append(textdata[i])
        