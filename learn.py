import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation as LDA

FILE = 'filtered_reviews.pkl'

data = []

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print '# features:', len(feature_names)

dates = []

with open(FILE) as f:
    while True:
        try:
            raw_data = pickle.load(f)
            data.append(raw_data['text'])
            dates.append(raw_data['date'])
        except:
            break

print '# reviews:', len(data)

print sorted(dates)[:5]

tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, \
        max_features=1000, stop_words='english')
tf = tf_vectorizer.fit_transform(data)
lda = LDA(n_topics=10, max_iter=5)
lda.fit(tf)
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, 20)

tfidf_vectorizer = TfidfVectorizer(stop_words='english', \
        max_df=0.95, min_df=5, max_features=1000)
tfidf = tfidf_vectorizer.fit_transform(data)
nmf = NMF(n_components=10, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, 20)
