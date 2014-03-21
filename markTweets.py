import bz2
import os
import json

events = {'BiarritzSurfFestival,France' : ['biarritz'], 'BastilleDay,France':['bastille'], 'BillabongProSurfing,SA' :['billabong'], 'CalgaryStampede,Canada' :['calgary', 'stampede'], 'ChristopherStreetDay,Cologne' : ['christopher','street', 'day'], 'CopenhagenJazzFestival': ['coppenhagen' ,'jazz'], 'ExitMusicFestival,Serbia' : ['exit', 'fest'], 'HemisFestival,Ladakh' : ['hemis', 'festival'], 'IndependenceDay,USA' : ['independence', 'day', 'usa'], 'LoveParade,Germany' : ['love','parade'], 'MangoFestival,Delhi' : ['mango', 'festival', 'delhi'], 'MontreuxJazzFestival,Swiss' : ['montreux', 'jazz'] , 'MunichOperaFestival' : ['munich', 'opera'], 'NagPanchami,India' : ['nag', 'panchami'], 'OlympicGames,London' : ['olympic'], 'PampalonaBullFestival,Spain' : ['pampalona', 'bull'], 'BoryeongMudFestival,SouthKorea' : ['boryeong','mud'], 'RathYatra,Puri': ['rath', 'yatra'], 'SingaporeFoodFestival' : ['singapore', 'food', 'fest'], 'SalzburgMusicFestival' : ['salzburg', 'fest'], 'TeejFestival': ['teej', 'festival'], 'TanabataFestival,Japan' : ['tanabata', 'fest'], 'TourdeFrance': ['tour', 'de', 'france'], 'WifeCarryingChampionship,Finland' : ['wife', 'carrying', 'championship'], 'Roskilde,Denmark' : ['roskilde', 'fest'], 'TInThePark,UK' : ['T in the park'], 'TInThePark' : ['Tinthepark'], 'Benicassism,Spain' : ['benicassism', 'fest'], 'RockNCokeMusicFestival,Istanbul' : ['rock\'n', 'coke'], 'GrassrootsEcoFestival,UK' : ['grassroot', 'fest'] , 'TheSecretGardenParty,UK' : ['secret', 'garden', 'party'], 'GlobalGathering,UK' : ['global', 'gathering'], 'AttackOnChurches,Garissa,Kenya' : ['church', 'garissa'], 'SpainItalyEuroCupFootball' : ['euro', 'spain', 'italy'], 'GlaxoSmithKlineFraud' : ['glaxo', 'smith', 'kline', 'fraud'], 'TruckBombing,Diwaniyah,Iraq' : ['diwaniyah', 'truck'], 'AntonioEsfandiariPoker' : ['esfandiari', 'poker'], 'TheShardTallestBuildingEurope' : ['shard', 'building'], 'EnriquePenaNietoInstitutionalRevolutionaryPartyPresident,Mexico' : ['presid', 'nieto'], 'FloodKrasnodarRussia' : ['krasnodar', 'flood'], 'EpiscopalChurchGayMarriages' : ['episcopal', 'gay'], 'S2012FifthMoon,Pluto' : ['s/2012', 'pluto'], '200KilledSiriyaArmy,Tremseh' : ['syria', 'army', 'tremseh'], 'SyriaViolenceMinisterOfDefenseKill' : ['minister', 'defense', 'syria'], 'KimJong-unSupremeLeaderMashalNorthKorea' : ['kim', 'jong', 'supreme', 'leader'], 'DarkKnightShoot,Aurora,Colorado' : ['dark', 'knight', 'aurora'], 'BusAccident,Nayarit,Mexico' : ['nayarit', 'accident'], 'PranabMukherjeePresident,India' : ['mukherjee', 'president'], 'JohnDramaniPresidentDeathPresidentJohnAttaMills,Ghana' : ['dramani', 'president'], 'IvicaDacicPrimeMinisterSerbia' : ['dacic', 'prime', 'minister'], 'CCC+EganJonesItaly' : ['ccc+', 'italy'], 'KhanunTropicalStorm,NorthKorea' : ['khanun', 'storm'], 'YeShiwenWorldRecord400m' : ['shiwen', 'record']}

def is_ascii(s):
    return all(ord(c) < 128 for c in s)
def markFile(f, path):
    global events
    total_path = 'markedData/totaldata/' + path
    if not os.path.exists(total_path): os.makedirs(total_path)
    total = open(total_path + f +'.txt', 'a')
    a = bz2.BZ2File(path + f)
    f1 = []
    f2 = []
    for x in events:
        f1.append(open('markedData/' + x + '/totaldata.txt', 'a'))
        f2.append(open('markedData/' + x + '/textdata.txt', 'a'))
    b = a.readline()
    while b != '':
        c = json.loads(b)
        if 'user' in c and c['user']['lang'] == 'en' and is_ascii(c['text']):
            total.write(b)
            text = c['text'].lower()
            cnt = 0
            for i in events:
                ad = 1
                for y in events[i]:
                    if y not in text:
                        ad = 0
                        break;
                if ad == 1:
                    f1[cnt].write(b)
                    f2[cnt].write(text + "\n")
                    print i
                cnt += 1
                
        b = a.readline()
    total.close()

parentdirectory = 'twitterlogs/markedData/totaldata/2012/07/'
subdirectories1 = ['0' + str(x) + '/' for x in range(1,10)] + [str(x) + '/' for x in range(10,32)]
subdirectories2 = ['0' + str(x) + '/' for x in range(10)] + [str(x) + '/' for x in range(10,24)]
for i in events:
    total_path = 'markedData/' + i
    if not os.path.exists(total_path): os.makedirs(total_path)
for i in subdirectories1:
    for j in subdirectories2:
        path = parentdirectory + i + j
        for root, dirs, filename in os.walk(path):
            for f in filename:
                markFile(f, path)

#for i in events:
#    total_path = 'markedData/' + i
#    if not os.path.exists(total_path): os.makedirs(total_path)
