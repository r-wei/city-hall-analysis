"""
http://scikit-learn.org/stable/auto_examples/text/document_clustering.html
adapted to work with documents from City Hall Monitor
=======================================
Clustering text documents using k-means
=======================================

This is an example showing how the scikit-learn can be used to cluster
documents by topics using a bag-of-words approach. This example uses
a scipy.sparse matrix to store the features instead of standard numpy arrays.

Two feature extraction methods can be used in this example:

  - TfidfVectorizer uses a in-memory vocabulary (a python dict) to map the most
    frequent words to features indices and hence compute a word occurrence
    frequency (sparse) matrix. The word frequencies are then reweighted using
    the Inverse Document Frequency (IDF) vector collected feature-wise over
    the corpus.

  - HashingVectorizer hashes word occurrences to a fixed dimensional space,
    possibly with collisions. The word count vectors are then normalized to
    each have l2-norm equal to one (projected to the euclidean unit-ball) which
    seems to be important for k-means to work in high dimensional space.

    HashingVectorizer does not provide IDF weighting as this is a stateless
    model (the fit method does nothing). When IDF weighting is needed it can
    be added by pipelining its output to a TfidfTransformer instance.

Two algorithms are demoed: ordinary k-means and its more scalable cousin
minibatch k-means.

Additionally, latent sematic analysis can also be used to reduce dimensionality
and discover latent patterns in the data.

It can be noted that k-means (and minibatch k-means) are very sensitive to
feature scaling and that in this case the IDF weighting helps improve the
quality of the clustering by quite a lot as measured against the "ground truth"
provided by the class label assignments of the 20 newsgroups dataset.

This improvement is not visible in the Silhouette Coefficient which is small
for both as this measure seem to suffer from the phenomenon called
"Concentration of Measure" or "Curse of Dimensionality" for high dimensional
datasets such as text data. Other measures such as V-measure and Adjusted Rand
Index are information theoretic based evaluation scores: as they are only based
on cluster assignments rather than distances, hence not affected by the curse
of dimensionality.

Note: as k-means is optimizing a non-convex objective function, it will likely
end up in a local optimum. Several runs with independent random init might be
necessary to get a good convergence.

"""

# Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
#         Lars Buitinck <L.J.Buitinck@uva.nl>
# License: BSD 3 clause

from __future__ import print_function

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans

import logging
from optparse import OptionParser
import sys
from time import time

import numpy as np

import psycopg2

from analyze_titles import *
import collections

import os


# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# parse commandline arguments
op = OptionParser()
op.add_option("--lsa",
              dest="n_components", type="int",
              help="Preprocess documents with latent semantic analysis.")
op.add_option("--no-minibatch",
              action="store_false", dest="minibatch", default=True,
              help="Use ordinary k-means algorithm (in batch mode).")
op.add_option("--no-idf",
              action="store_false", dest="use_idf", default=True,
              help="Disable Inverse Document Frequency feature weighting.")
op.add_option("--use-hashing",
              action="store_true", default=False,
              help="Use a hashing feature vectorizer")
op.add_option("--n-features", type=int, default=10000,
              help="Maximum number of features (dimensions)"
                   " to extract from text.")
op.add_option("--verbose",
              action="store_true", dest="verbose", default=False,
              help="Print progress reports inside k-means algorithm.")

print(__doc__)
op.print_help()

(opts, args) = op.parse_args()
if len(args) > 0:
    op.error("this script takes no arguments.")
    sys.exit(1)

###############################################################################

#Function for clearly printing a dictionary's values
def dictPrint(dictIn):
  try: 
    for attribute, value in dictIn.items():
      print('{} : {}'.format(attribute, value))
    print('\n')
  except:
    f1.write('\n =============================== \n PRINTING ISSUE \n =============================== \n')

###############################################################################
print("loading city hall monitor documents")

documents = []
titles = []
#Connect to the database
try:
    conn = psycopg2.connect(database='cityhallmonitor',user='cityhallmonitor',password='cityhallmonitor',host='localhost')
           #psycopg2.connect("dbname='cityhallmonitor' user='Bomani' host='localhost' password='wolfbite1'")
    print("Database Connected!")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()
t0 = time()
# cur.execute('select matter_attachment_id, title, text from cityhallmonitor_document')
cur.execute('select matter_attachment_id, title, text from cityhallmonitor_matter m , cityhallmonitor_matterattachment ma , cityhallmonitor_document d where m.id=ma.matter_id and ma.id=d.matter_attachment_id')

#make a dictionary of keys:values - matter_id:(title, text)
documentDict = {}
for row in cur:
  documentDict[row[0]] = (row[1], row[2])

print("%d documents" % len(documentDict.keys()))
print()
print("done in %fs" % (time() - t0))

t0 = time()
documentDict = group_titles(documentDict) #returns a dictionary of matter_id: (title, text, truncated_title, T/F is_this_doc_grouped_via_title_analysis)
keys = documentDict.keys()

#create a dictionary of docs not organized by title analysis
remaining_docs = dict()
for key in keys:
    if documentDict[key][3] == False:
        remaining_docs[key] = documentDict[key]

remaining_keys = list(remaining_docs.keys())

print("There are " + str(len(remaining_keys)) + " documents remaining.")
print("Title analysis done in %fs" % (time() - t0))

labels = None # not sure what the analog to labels is for our dataset
true_k = 20 # is there a smarter way to get this from our documents?

print("Extracting features from the training dataset using a sparse vectorizer")
t0 = time()
if opts.use_hashing:
    if opts.use_idf:
        # Perform an IDF normalization on the output of HashingVectorizer
        hasher = HashingVectorizer(n_features=opts.n_features,
                                   stop_words='english', non_negative=True,
                                   norm=None, binary=False)
        vectorizer = make_pipeline(hasher, TfidfTransformer())
    else:
        vectorizer = HashingVectorizer(n_features=opts.n_features,
                                       stop_words='english',
                                       non_negative=False, norm='l2',
                                       binary=False)
else:
    vectorizer = TfidfVectorizer(max_df=0.3, max_features=opts.n_features,
                                 min_df=0.2, stop_words='english',
                                 use_idf=opts.use_idf)#still produces some really big non-meaningful groups

remaining_text = []
for key in remaining_keys:
    remaining_text = remaining_text + [remaining_docs[key][1]]

X = vectorizer.fit_transform(remaining_text) #run kmeans on text of remaining_docs only

print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X.shape)
print()

if opts.n_components:
    print("Performing dimensionality reduction using LSA")
    t0 = time()
    # Vectorizer results are normalized, which makes KMeans behave as
    # spherical k-means for better results. Since LSA/SVD results are
    # not normalized, we have to redo the normalization.
    svd = TruncatedSVD(opts.n_components)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)

    X = lsa.fit_transform(X)

    print("done in %fs" % (time() - t0))

    explained_variance = svd.explained_variance_ratio_.sum()
    print("Explained variance of the SVD step: {}%".format(
        int(explained_variance * 100)))

    print()


###############################################################################
# Do the actual clustering

if opts.minibatch:
    km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                         init_size=1000, batch_size=1000, verbose=opts.verbose)
else:
    km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1,
                verbose=opts.verbose)

print("Clustering sparse data with %s" % km)
t0 = time()
km.fit(X)
print("done in %0.3fs" % (time() - t0))
print()

if labels:
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
    print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
    print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
    print("Adjusted Rand-Index: %.3f"
          % metrics.adjusted_rand_score(labels, km.labels_))
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X, km.labels_, sample_size=1000))
else:
    print("Can't compute accuracy metrics without labels")

print()

#add centroid assignment to remaining_docs dictionary
centroid_labels = km.labels_
for j in range(len(centroid_labels)):
    tup = centroid_labels[j], 
    remaining_docs[remaining_keys[j]] = remaining_docs[remaining_keys[j]] + tup 

counter = collections.Counter(centroid_labels)

t0 = time()
if not opts.use_hashing:
    res_file = open('cluster_results', 'w')
    res_file.write("Top terms per cluster:")

    if opts.n_components:
        original_space_centroids = svd.inverse_transform(km.cluster_centers_)
        order_centroids = original_space_centroids.argsort()[:, ::-1]
    else:
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names()
    centroids = km.cluster_centers_
    for i in range(true_k):
        res_file.write("\n Cluster %d:" % i)
        for ind in order_centroids[i, :10]:
            res_file.write(' %s' % terms[ind])
        res_file.write('\t - \t %d docs' % counter[i])

	#print titles of the 5 docs closest to the centroid
        distances = (np.power(X.todense() - centroids[i],2)).sum(axis=1)
        order_dist = np.argsort(distances, axis=0)
        for j in range(5):
            res_file.write('\n \t'+ remaining_docs[remaining_keys[order_dist[j]]][0]) #print jth closest doc to centroid
            res_file.write('\n \t'+ remaining_docs[remaining_keys[order_dist[-j]]][0]) #print jth furthest doc
    res_file.close()

for key in remaining_keys:
  label = remaining_docs[key][4]
  # Write txt to file
  directory = 'newClusters/cluster-{}'.format(label)
  if not os.path.exists(directory):
    os.makedirs(directory)

  filename = directory + '/{}.txt'.format(key)
  file_ = open(filename, 'w')
  file_.write(remaining_docs[key][1])
  file_.close()

print("done writing to files in %fs" % (time() - t0))


#Run Analysis on Clusters
for i in range(true_k):
  clusterDict = {}
  for key in remaining_keys:
    if(remaining_docs[key][4] == i):
      clusterDict[key] = remaining_docs[key]

  print('\n#################################')
  print('########## Cluster {} ###########'.format(i))
  print('#################################\n')
  analyzedCluster = group_titles(clusterDict)
  print('\n')

