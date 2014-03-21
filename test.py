

from sklearn.feature_extraction.text import onlineTfidfVectorizer, TfidfVectorizer, CountVectorizer
#from sklearn.utils.fixes import Counter

#a = Counter()
#a1 = "hello is anybody anybody in there?"
#a2 = "hello hello how are you anybody anybody today"
#a3 = "today is a wonderful day hello"
#b = Counter(analyze(a1))
#print b
#a.update(b)
#print a
#b = Counter(analyze(a2))
#print b
#a.update(b)
#print a.most_common()
vectorizer = onlineTfidfVectorizer(min_df = 1, smooth_idf=True, stop_words='english')
corpus = [
          'italy italy italy italy italy set for another cathartic experience #Italy #Spain #Euro2012']
X = vectorizer.fit_transform(corpus)
print vectorizer.vocabulary_
print vectorizer.document_counts
print vectorizer.idf_
print X.toarray()
#vecto = onlineTfidfVectorizer(min_df=1, smooth_idf=False)
#Y = vecto.fit_transform(corpus[:2])
#Y = vecto.transform(corpus[2:3])
#Y = vecto.transform(corpus[3:])
#print Y.toarray()
#print vecto.vocabulary_
#print vecto.document_counts
#print vecto.idf_
#vectorizer.vocabulary_['Dilpreet'] = 7
#print vectorizer.vocabulary_
#
from sklearn.feature_extraction.text import TfidfTransformer
#trans = TfidfTransformer()

#from lshash import LSHash
#from scipy.sparse import csr_matrix
#from storage import storage, QueueDictStorage, queueStorage
#a = queueStorage(maxsize = 100)

#a1 = csr_matrix([1,2,3,4,5,6,7,8])
#a2 = csr_matrix([2,3,4,5,6,7,8,9])
#a3 = csr_matrix([10,12,99,1,5,31,2,3])
#print a1.toarray()
#lsh = LSHash(6, 8, matrices_filename="test.npz", max_queue_size=10)
#a = (1,2)
#b = (2,3)
#c = (3,4)
#lsh.index(a1, extra_data=a)
#lsh.index(a2, extra_data=b)
#lsh.index(a3, extra_data=c)
#lsh.index(a1)
#lsh.index(a2)
#lsh.index(a3)
#print lsh.hash_tables[0].keys()
#print lsh.hash_tables[0].storage['110111'].getArray()[0][0][0]
#((a,b),c) = lsh.arpoxNN(csr_matrix([1,2,3,5,6,7,8,9]))
#print b
#lsh.index(a[0], extra_data="hellp")
#an = lsh.arpoxNN(csr_matrix([1,2,3,5,6,7,8,9]))
#print an
#lsh.hash_tables = []
#x = storage({'dict': None}, 0)
#x.storage= {'010011': [(10, 12, 99, 1, 5, 31, 2, 3)], '110111': [((1, 2, 3, 4, 5, 6, 7, 8), 'a'), ((2, 3, 4, 5, 6, 7, 8, 9), 'b')]}
#lsh.hash_tables.append(x)
#print lsh.query([1,2,3,4,5,6,7,7])