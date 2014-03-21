import json
f = 'geodata.txt'
f2 = 'newyork.txt'
f2 = open(f2, 'w')
with open(f) as infile:
    for line in infile:
        c = json.loads(line)
        if c['place'] != None:
            if 'name' in c['place']:
                if c['place']['name'].lower() == 'new york':
                    f2.write(json.dumps(c) + '\n')
f2.close()