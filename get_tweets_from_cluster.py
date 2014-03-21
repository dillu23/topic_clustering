import json

f = open('result3.txt')
a = f.readline()
while(a):
    b = json.loads(a)
    a = f.readline()
c = b.keys()
c.sort(key = lambda x : -1 * len(b[x]))

c = c[:100]
k = 0
for i in c:
    k = k+1
    f = open('processedtweets.txt')
    a = f.readline()
    f2 = open(str(k) + '.txt', 'w')
    while(a):
        d = json.loads(a)
        if d['id'] in b[i]:
            try:
                f2.write(d['text'] + "\n")
            except:
                print "lol"
        a = f.readline()

            