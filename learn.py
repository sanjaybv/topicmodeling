import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

FILE = 'filtered_reviews.pkl'

data = []

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


with open(FILE) as f:
    while True:
        try:
            data.append(pickle.load(f)['text'])
        except:
            break

print len(data)

tfidfVectorizer = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=5, max_features=1000)
tfidf = tfidfVectorizer.fit_transform(data)

lda = LDA(n_topics=15)
lda.fit(tfidf)

tf_feature_names = tfidfVectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, 20)
