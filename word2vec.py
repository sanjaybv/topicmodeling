from gensim.models import Word2Vec
import os
import codecs
import re

MODEL_PATH = 'data/word2vec.bin'

token_pattern = re.compile(r"\b\w\w+\b", re.U)

def custom_tokenizer(string, min_term_length=2):
	return [x.lower() for x in token_pattern.findall(string) 
                if len(x) >= min_term_length and x[0].isalpha()]

class Documents(object):
    def __init__(self, dirname, stopwords):
        self.dirname = dirname
        self.stopwords = stopwords

    def __iter__(self):
        for subdir, dirs, files in os.walk(self.dirname):
            if not files:
                continue

            for fname in files:
                filepath = os.path.join(subdir, fname)
                fin = codecs.open(filepath, 'r', encoding="utf8", errors='ignore')
		body = fin.read().lower().strip()
                
                tokens = []
                for token in custom_tokenizer(body):
                    if token in self.stopwords:
                        tokens.append('<stopword>')
                    else:
                        tokens.append(token)
                yield tokens

class Coherence(object):
    def __init__(self, docs_dir, stopwords):
        self.model = None
        self.docs_dir = docs_dir
        self.stopwords = stopwords

    def similarity_score(self, data):
        if self.model is None:
            self.build_model()
        
        score = 0.0
        for topic_words in data:
            score += self.eval_topic(topic_words)
        return score / len(data)

    def eval_topic(self, words):
        score = 0.0
        count = 0
        for w1 in words:
            for w2 in words:
                try:
                    score += self.model.similarity(w1, w2)
                    count += 1
                except:
                    print 'sim fail', w1, w2
                    pass
        if not count:
            return 0.0
        return score / count


    def build_model(self):
        if os.path.isfile(MODEL_PATH):
            self.model = Word2Vec.load(MODEL_PATH)
            return

        print 'building w2v model'
        docs = Documents(self.docs_dir, self.stopwords)
        self.model = Word2Vec(docs, size=100, min_count=2, window=5, workers=4)
        self.model.save(MODEL_PATH)


