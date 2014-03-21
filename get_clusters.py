import json

f = open('tweets_iddata.txt')
a = f.readline()
l = json.loads(a)
a = f.readline()
u = json.loads(a)
f.close()

def find_file(a):
	global u
	global l
	for x in l:
		if(int(l[x]) >= a and int(u[x]) <= a):
			return x

def get_cluster(a, r):
	a = [int(x) for x in a]
	b = set(a)
	#print b
	files = set()
	f2 = open(r, 'w')
	for x in a:
		files.add(find_file(x))
	for x in files:
		print x
		f = open('processed_tweets/' + str(x))
		c = f.readline()
		while(c):
			d = json.loads(c)
			if (int(d['id']) in b):
				print d['text']
				f2.write(d['text'])
			c = f.readline()
	f2.close()


f = open('result.txt')
a = f.readline()
b = a
while(a):
	b = a
	a = f.readline()

b = json.loads(b)
c = b.keys()
c.sort(key = lambda x : -1 * len(b[x]))

c = c[:100]
i = 0
for x in c:
	get_cluster(b[x], "clusters/" + str(i) + ".txt")
	i = i+1
