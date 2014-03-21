import geohash
a = ['dre9', 'drft', 'dr8g', 'drfw', 'dr8j', 'dr8k', 'drfz', 'dre2', 'dr8n', 'dre7', 'dr8s', 'drdm', 'dr8v', 'drdk', 'dr8t', 'dr8u', 'dr95', 'dr8y', 'dr7b', 'dr9h', 'drk0', 'drhp', 'dre3', 'dpxf', 'dr7r', 'dr7k', 'dr7j', 'dr7h', 'dr7m', 'drk8', 'dr5x', 'dr5z', 'dr7w', 'dpxu', 'dpxv', 'dr7t', 'dr5q', 'dr5r', 'dr9g', 'dr5w', 'dre0', 'dr8h', 'drgw', 'drf5', 'dr9k', 'drd9', 'dr9e', 'dres', 'dreh', 'drek', 'dr8e', 'dr85', 'dr9t', 'dr9v', 'dree', 'dred', 'dr9s', 'dr6g', 'drfh', 'dpxg', 'dr72', 'dr77', 'dr75', 'dr78']
y1 = max(a, key = lambda x : geohash.decode_exactly(x)[0] + geohash.decode_exactly(x)[2])
print geohash.decode_exactly(y1)[0] + geohash.decode_exactly(y1)[2]
y1 = max(a, key = lambda x : geohash.decode_exactly(x)[1] + geohash.decode_exactly(x)[3])
print geohash.decode_exactly(y1)[1] + geohash.decode_exactly(y1)[3]
y1 = min(a, key = lambda x : geohash.decode_exactly(x)[0] - geohash.decode_exactly(x)[2])
print geohash.decode_exactly(y1)[0] - geohash.decode_exactly(y1)[2]
y1 = min(a, key = lambda x : geohash.decode_exactly(x)[1] - geohash.decode_exactly(x)[3])
print geohash.decode_exactly(y1)[1] + geohash.decode_exactly(y1)[3]

