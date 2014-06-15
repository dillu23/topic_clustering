import json

def get_cluster(x,c,clusters,  tweets):
    f = open('clusters/' +str(x) + '.txt', 'w')
    for y in clusters[c[x]]:
        f.write(tweets[y] + '\n')
    f.close()


tweets = {}

f = open('../tweets1_1402240519.42_.txt')

a = f.readline()
while(a):
    b= json.loads(a)
    for x in b:
        tweets[x] = b[x]
    a = f.readline()

f = open('result.txt')
a = f.readline()
while(a):
    b = a
    a = f.readline()
clusters = json.loads(b)

c = clusters.keys()
c.sort(key = lambda x : -1 * len(clusters[x]))
#c = c[:100]
d = []
for x in c:
    if len(clusters[x])>=10:
        d.append(x)
c = d
for i in range(len(c)):
    print len(clusters[c[i]])
    get_cluster(i,c, clusters, tweets)
