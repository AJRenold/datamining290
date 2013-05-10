## Extract top 20 terms by TfIdf per Business Category

import os
import json
from itertools import islice
import re
from collections import Counter, defaultdict
from math import log
import numpy as np

yelp_dir = os.getcwd() + "/yelp_phoenix_academic_dataset_2"
for dirpath, dirname, filenames in os.walk(yelp_dir):
    files = filenames
data_files = [ f for f in files if f[-5:] == '.json' ]
print data_files

review_json = open(yelp_dir + "/" + data_files[2])
reviews = [ json.loads(line) for line in islice(review_json,None) ]
#review_df = pd.DataFrame(reviews_for_df)
#print reviews[0]

business_json = open(yelp_dir + "/" + data_files[0])
business_json_list = [ json.loads(line) for line in islice(business_json,None) ]

business_dict = {}
for biz in business_json_list:
    business_dict[biz['business_id']] = biz


def get_stop_names():
    f = open('stop_names.csv')

    stop_names = {}

    for line in islice(f,None):
        word = line.lower().strip()[line.find(',')+1:]
        if word not in stop_names:
            stop_names[word] = True

    return stop_names

stop_names = get_stop_names()

def tokenize(doc):

    text = re.sub(r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?]))", \
            "webURL",doc)
    text = re.sub(r"[\n\.,;\!\?\(\)\[\]\*/:~]"," ",doc)
    text = re.sub(r"(\b[\d]+\b|\b[\d]+[a-z]+\b)"," ",text)
    text = re.sub(r"['\-\"]","",text)
    words = text.lower().split(" ")

    clean_words = []
    for word in words:
        if word != '' and word != ' ' and len(word) > 1:
            if word in stop_names:
                pass
            elif '$' in word:
                clean_words.append('priceMention')
            else:
                clean_words.append(word)

    return clean_words

def calc_idf(documents):
    
    binary_word_count = Counter()
    num_docs = len(documents)

    for doc in documents:
        for word in set(doc):
            binary_word_count[word] += 1

    idf = {}
    for word, count in binary_word_count.iteritems():
        if count > 5:
            idf[word] = log( float(num_docs) / count )

    return idf

def calc_tfidfs(document,idf):

    word_counts = Counter(document)
    tfidfs = []
    for word, count in word_counts.iteritems():
        if word in idf:
            tfidf = float(count) * idf[word]
            tfidfs.append((word, tfidf))
    return tfidfs

reviews_by_cat = defaultdict(list)

## isolate 'Restaurants'
for review in islice(reviews,None):
    for cat in business_dict[review['business_id']]['categories']:
        reviews_by_cat[cat].append(tokenize(review['text']))

print "data loaded"

cat_top_tfidfs = defaultdict(dict)
for cat, reviews in islice(reviews_by_cat.iteritems(),None):
    idf = calc_idf(reviews)
    cat_tfidfs = defaultdict(list)
    for review in reviews:
        tfidfs = calc_tfidfs(review, idf)
        for pair in tfidfs:
            cat_tfidfs[pair[0]].append(pair[1])

    mean_tfidf = {}
    for word, tfidf_list in cat_tfidfs.iteritems():
        mean_tfidf[word] = np.mean(tfidf_list)

    list_of_tfidfs = [ [ mean, word ] for word, mean in mean_tfidf.iteritems() ]
    list_of_tfidfs.sort(reverse=True)
    
    cat_top_tfidfs[cat] = list_of_tfidfs[:20]

#print json.dumps(cat_top_tfidfs, sort_keys=True, indent=4, separators=(',', ': '))

json_for_viz = open('category_top_tfidfs.json','w')
json_for_viz.write(json.dumps(cat_top_tfidfs, sort_keys=True, indent=4, separators=(',', ': ')))
