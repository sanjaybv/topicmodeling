import json
from pprint import pprint
import cPickle as pickle

FILE_BUSINESS = 'yelp_academic_dataset_business.json'
FILE_REVIEWS = 'yelp_academic_dataset_review.json'
FILE_FILTERED_REVIEWS = 'filtered_reviews.pkl'

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

reviews_count = 0

with open(FILE_REVIEWS) as data_file:
    with open(FILE_FILTERED_REVIEWS, 'wb') as filtered_data:
        for i, line in enumerate(data_file):
            data = json.loads(line)
            if data['business_id'] in business_ids:
                pickle.dump(data, filtered_data)
                reviews_count += 1
            if i == 100000:
               break
            print '\r', i,
        print

print '# relevant reviews:', reviews_count

