import json
f = 'data.txt'
all = []
with open(f) as infile:
    for line in infile:
        line = json.loads(line)
        a = ""
        print line
        i = 0
        for x in line:
            if i==0:
                a = x
                i = 1
            else:
            #print x
                a = a + " , " + x
        print a
        all.append(a)
print all