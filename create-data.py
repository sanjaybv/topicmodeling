import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import numpy as np
import pickle

DATA_DIR = 'data/raw/'
WINDOW_FILE = 'data/window-models.pkl'
YEARS = xrange(2008, 2017)

class WindowModel(object):

    def __init__(self, num_topics = 17):
        self.num_topics = 17

    def build(self, year, files):
        # apply tfidf
        tfidf = TfidfVectorizer(
                input='filename', 
                stop_words='english', 
                strip_accents='unicode',
                min_df=2,
                norm='l2',
                max_features=1000
                )
        self.tfidf_matrix = tfidf.fit_transform(files)

        vocab = tfidf.vocabulary_
        self.cur_terms = ['']*len(vocab)
        for key, val in vocab.iteritems():
            self.cur_terms[val] = key

        # apply NMF
        nmf = NMF(
                init='random',
                n_components=self.num_topics
                )
        self.W = nmf.fit_transform(self.tfidf_matrix)
        self.H = nmf.components_


class DynamicModel(object):
    def __init__(self):
        self.B = None
        self.terms = {}

    def build(self, window_models):
        for year in sorted(window_models.keys()):
            window_topic = window_models[year]
            window_topic.H

def build_window_models():

    if os.path.isfile(WINDOW_FILE):
        print 'loading window models'
        with open(WINDOW_FILE) as window_file:
            return pickle.load(window_file)

    window_models = {}
    print 'building window topic models...'
    for subdir, dirs, files in os.walk(DATA_DIR):
        if not files:
            continue
        print subdir
        cur_dir = int(subdir.split('/')[-1])
        filepaths = [os.path.join(subdir, f) for f in files]

        wm = WindowModel()
        wm.build(cur_dir, filepaths)
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
