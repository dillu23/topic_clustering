import json
import csv
events = ['CalgaryStampede,Canada', 'MontreuxJazzFestival,Swiss', 'GlobalGathering,UK', 'SpainItalyEuroCupFootball', 'GlaxoSmithKlineFraud', 'SyriaViolenceMinisterOfDefenseKill', 'KimJong-unSupremeLeaderMashalNorthKorea', 'DarkKnightShoot,Aurora,Colorado', 'PranabMukherjeePresident,India', 'YeShiwenWorldRecord400m']
counter= {}
f3 = open('clusters.txt', 'r')
clusters = json.loads(f3.readline())
inv_index = json.loads(f3.readline()) 
inv2_index = {}
for i in inv_index:
    inv2_index[int(i)] = inv_index[i]
k = inv2_index.keys()
k.sort()

f = 'testset.txt'
f1 = open('heirarchichal_clustering2.csv' , 'w')
wr = csv.writer(f1)
cluster_topic = {}
with open(f) as infile:
    for line in infile:
        line = json.loads(line)
        cluster_topic[int(line['id'])] = line['topic_class']

for i in k:
    wr.writerow([i] + [cluster_topic[i]] + [inv2_index[i]])
f1.close()