# Dynamic Topic Modeling

1. Download Yelp Dataset. Copy `yelp_academic_dataset_review.json` and `yelp_academic_dataset_review.json` to project folder.
2. Then run `python filter.py`. This filters the data set and creates a output data folder and a `reviews_restaurants.pkl` file.
3. Then run `python dynamic_modeling.py`. This will show the dynamic topics that are created.

The file `reviews_restaurants.pkl` contains two python maps, first which maps review ids to business ids and the second which maps business ids to business names.

# Contributors
Sanjay, Soundar and Chandan
