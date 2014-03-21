import os
import json

events = {'CalgaryStampede,Canada' :300,'MontreuxJazzFestival,Swiss' : 200 ,'GlobalGathering,UK' :1000, 'SpainItalyEuroCupFootball' : 500, 'GlaxoSmithKlineFraud' : 200, 'SyriaViolenceMinisterOfDefenseKill' : 1000, 'KimJong-unSupremeLeaderMashalNorthKorea' : 200, 'DarkKnightShoot,Aurora,Colorado' : 500, 'PranabMukherjeePresident,India' : 250, 'YeShiwenWorldRecord400m' : 200}
counter = {}
for i in events:
    counter[i] = 0
f = 'markedData/totalled1.txt'
f2 = open('testset.txt', 'a')
with open(f) as infile:
    for line in infile:
        c = json.loads(line)
        if c['topic_class'] in events.keys() and counter[c['topic_class']] < events[c['topic_class']]:
            f2.write(json.dumps(c) + '\n')
            counter[c['topic_class']] = counter[c['topic_class']] + 1
            
f2.close()
f = 'markedData/totalled.txt'
f2 = open('testset.txt', 'a')
with open(f) as infile:
    for line in infile:
        c = json.loads(line)
        if c['topic_class'] in events.keys() and counter[c['topic_class']] < events[c['topic_class']]:
            f2.write(json.dumps(c) + '\n')
            counter[c['topic_class']] = counter[c['topic_class']] + 1
            
f2.close()