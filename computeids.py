import json
import csv
events = ['CalgaryStampede,Canada', 'MontreuxJazzFestival,Swiss', 'GlobalGathering,UK', 'SpainItalyEuroCupFootball', 'GlaxoSmithKlineFraud', 'SyriaViolenceMinisterOfDefenseKill', 'KimJong-unSupremeLeaderMashalNorthKorea', 'DarkKnightShoot,Aurora,Colorado', 'PranabMukherjeePresident,India', 'YeShiwenWorldRecord400m']
counter= {}
f3 = open('clusters.txt', 'r')
clusters = json.loads(f3.readline())
inv_index = json.loads(f3.readline())
k = inv_index.keys()

c_matrix = [0 for i in range(len(clusters))]

for i in range(len(clusters)):
    c_matrix[i] = [0 for j in range(len(events))]
print c_matrix
#fw = [0 for i in range(len(clusters))]
#for i in clusters:
#    fw[int(i)] = open('clusters/' + str(i) + '.txt', 'a')
f = 'testset.txt'
f1 = open('c_matrix.csv' , 'w')
wr = csv.writer(f1)
wr.writerow([" "] + events)
with open(f) as infile:
    for line in infile:
        c = json.loads(line)
        i = inv_index[str(c['id'])]
#        d = {}
#        d['text'] = c['text']
#        d['topic_class'] = c['topic_class']
#        fw[i].write(json.dumps(d) + '\n')
        c_matrix[int(i)][events.index(c['topic_class'])] = c_matrix[int(i)][events.index(c['topic_class'])] + 1

c_matrix.sort(key = lambda x : - sum(x))
for i in range(len(c_matrix)):
    wr.writerow([i] + c_matrix[i])

f1.close()

print c_matrix
