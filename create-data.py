import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import numpy as np
import pickle
import bottleneck

DATA_DIR = 'data/raw/'
WINDOW_FILE = 'data/window-models.pkl'
YEARS = xrange(2008, 2017)
STOPWORDS_FILE = 'data/stopwords.txt'

class WindowModel(object):

    def __init__(self, num_topics = 17):
        self.num_topics = 17


    def build(self, year, files, stopwords):
        
        self.year = year
        
        # apply tfidf
        tfidf = TfidfVectorizer(
                input='filename', 
                stop_words=stopwords, 
                strip_accents='unicode',
                min_df=2,
                norm='l2',
                max_features=1000
                )
        self.tfidf_matrix = tfidf.fit_transform(files)

        vocab = tfidf.vocabulary_
        self.terms = ['']*len(vocab)
        for key, val in vocab.iteritems():
            self.terms[val] = key

        # apply NMF
        nmf = NMF(
                init='random',
                n_components=self.num_topics
                )
        self.W = nmf.fit_transform(self.tfidf_matrix)
        self.H = nmf.components_

    def get_top_terms(self, num_top):
        # topic_name --> list(term, value)
        top_terms = {}

        # get top values for each row of H
        for topic_index, topic_row in enumerate(self.H):
            cur_terms = []
            top_indices = np.array(topic_row).argsort()[-num_top:]
            for i in top_indices:
                cur_terms.append((self.terms[i], topic_row[i]))

            topic_name = '{0}-{1:02d}'.format(self.year, topic_index)
            top_terms[topic_name] = cur_terms

        return top_terms



class DynamicModel(object):
    def __init__(self, num_top=10, num_topics=17):
        self.B = None
        self.terms = {}         # term --> index in B
        self.num_top = num_top
        self.num_topics = num_topics

    def build_b_matrix(self, window_models):

        # get top terms across all windows
        topic_docs = {}
        for year in sorted(window_models.keys()):
            window_topic = window_models[year]
            top_terms = window_topic.get_top_terms(self.num_top)
            topic_docs.update(top_terms)
            for topic_name, topic_terms in top_terms.iteritems():
                for term in topic_terms:
                    if term[0] not in self.terms:
                        self.terms[term[0]] = len(self.terms)
       
        # concat H matrix to B
        for topic_name, topic_terms in topic_docs.iteritems():
            topic_doc = np.zeros((len(self.terms)))
            for term, value in topic_terms:
                topic_doc[self.terms[term]] = value
            if self.B is None:
                self.B = topic_doc
            else:
                self.B = np.vstack((self.B, topic_doc))

    def build(self, window_models):

        # build B matrix
        self.build_b_matrix(window_models)

        # apply NMF again
        nmf = NMF(
                init='random',
                n_components=self.num_topics
                )
        self.U = nmf.fit_transform(self.B)
        self.V = nmf.components_
        

def build_window_models():

    if os.path.isfile(WINDOW_FILE):
        print 'loading window models'
        with open(WINDOW_FILE) as window_file:
            return pickle.load(window_file)

    with open(STOPWORDS_FILE) as f:
       stopwords = set(f.read().split())

    window_models = {}
    print 'building window topic models...'
    for subdir, dirs, files in os.walk(DATA_DIR):
        if not files:
            continue
        print subdir
        cur_dir = int(subdir.split('/')[-1])
        filepaths = [os.path.join(subdir, f) for f in files]

        wm = WindowModel()
        wm.build(cur_dir, filepaths, stopwords)
        window_models[cur_dir] = wm

    with open(WINDOW_FILE, 'wb') as window_file:
        pickle.dump(window_models, window_file)

    print '...done'
    return window_models

def main():

    # build individial window topic models
    window_models = build_window_models()

    # build dynamic topic model from window models
    dynamic_model = DynamicModel()
    dynamic_model.build(window_models)

    # show U matrix


if __name__ == '__main__':
    main()
