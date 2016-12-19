import json
import uuid
import os
import tempfile
from collections import Counter

import pickle

FILE_BUSINESS = 'yelp_academic_dataset_business.json'
FILE_REVIEWS = 'yelp_academic_dataset_review.json'
FILE_FILTERED_REVIEWS = 'filtered_reviews.pkl'
FILE_REVIEW_BUS = 'data/reviews_restaurants.pkl'
DIR = 'data/raw/'

# get business ids of the restaurants category
restaurants = {}
with open(FILE_BUSINESS) as data_file:
    for i, line in enumerate(data_file):
        data = json.loads(line)
        #print data['categories']
        if 'Restaurants' in data['categories']:
            bid = data['business_id'].encode('utf-8')
            bname = data['name'].encode('utf-8')
            restaurants[bid] = bname
        if i == 1000:
            pass#break
print '# restaurants:', len(restaurants)
#bid_iter = iter(restaurants)
#print 'some bids:', [next(bid_iter) for _ in xrange(5)]

review_to_bid = {}
reviews_count = 0

reviews = []
with open(FILE_REVIEWS) as data_file:
    for review_num, line in enumerate(data_file):
        print '\rreading review_num:', review_num,
        reviews.append(line)
        #if review_num >= 100000:
        #    break
print '\ndone reading reviews\n'

print 'calculating top 10 restaurants'
bid_count = Counter()
for review in reviews:
    review = json.loads(review)
    bid = review['business_id'].encode('utf-8')
    if bid in restaurants:
        bid_count.update([bid])

common_restaurants = dict(bid_count.most_common(10))
common_restaurants_names = {}
print '--10 most common restaurants--'
for bid, count in common_restaurants.iteritems():
    common_restaurants_names[bid] = restaurants[bid]
    print restaurants[bid], '-', count

print

print 'writing filtered data to {}'.format(DIR)
for review_num, review in enumerate(reviews):
    review = json.loads(review)
    bid = review['business_id'].encode('utf-8')
    if bid in common_restaurants_names:
        review_year = review['date'].split('-')[0]
        if int(review_year) >= 2008:
            reviews_count += 1
            review_dir = DIR + review_year + '/'
            review_filename = 'review'+str(review_num)
            review_to_bid[review_filename] = str(bid)
            if not os.path.exists(review_dir):
                os.makedirs(review_dir)
            review_path = review_dir + review_filename + '.txt'

            with open(review_path, 'w') as review_file:
                review_file.write(review['text'].encode('utf-8'))

with open(FILE_REVIEW_BUS, 'w') as rb_file:
    pickle.dump(review_to_bid, rb_file)
    pickle.dump(common_restaurants_names, rb_file)

print 'done\n'
print '# relevant reviews:', reviews_count
