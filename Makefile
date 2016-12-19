clean:
	rm data/*.pkl
	rm *.pyc

clean-all: clean
	rm -rf data/raw
	rm data/word2vec.bin
