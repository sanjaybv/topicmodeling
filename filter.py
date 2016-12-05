import json
import uuid
import os
import tempfile

from pprint import pprint
import cPickle as pickle

FILE_BUSINESS = 'yelp_academic_dataset_business.json'
FILE_REVIEWS = 'yelp_academic_dataset_review.json'
FILE_FILTERED_REVIEWS = 'filtered_reviews.pkl'
DIR = 'data/'

# get business ids of the restaurants category
business_ids = set()
with open(FILE_BUSINESS) as data_file:
    for i, line in enumerate(data_file):
        data = json.loads(line)
        #print data['categories']
        if 'Restaurants' in data['categories']:
            business_ids.add(data['business_id'])
        if i == 1000:
            pass#break
print '# restaurants:', len(business_ids)

review_to_bid = {}
reviews_count = 0

with open(FILE_REVIEWS) as data_file:
    for review_num, line in enumerate(data_file):
        print '\r processing review_num:', review_num,
        data = json.loads(line)
        if data['business_id'] in business_ids:
            reviews_count += 1
            review_year = data['date'].split('-')[0]
            review_dir = DIR + review_year + '/'
            review_filename = 'review'+str(review_num)
            review_to_bid[review_filename] = str(data['business_id'])
            if not os.path.exists(review_dir):
                os.makedirs(review_dir)
            review_path = review_dir + review_filename + '.txt'

            with open(review_path, 'w') as review_file:
                review_file.write(data['text'].encode('utf-8'))
        if review_num >= 100000:
            break

print '# relevant reviews:', reviews_count
