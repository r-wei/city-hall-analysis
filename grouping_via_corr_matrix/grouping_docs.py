#We apply ideas from ch 3 of Programming Collective Intelligence to texts from documents in city hall monitor.
#Namely, we construct the correlation matrix of keywords vs documents and see what that can teach us about organizing/grouping the documents.

import csv, collections
import numpy as np
from numpy import linalg
from nltk.tokenize import RegexpTokenizer
from scipy.cluster.vq import vq, kmeans2, whiten
from scipy.cluster.vq import vq, kmeans2, whiten
from sklearn.cluster import KMeans
import psycopg2
import time

#Connect to the database
try:
    conn = psycopg2.connect("dbname='cityhallmonitor' user='Bomani' host='localhost' password='wolfbite1'")
    print("Database Connected!")
except:
    print("I am unable to connect to the database")

#Create a cursors, query a table, & save the results into a list.
cur = conn.cursor()
cur.execute("""SELECT text from cityhallmonitor_document limit 100""")
texts = cur.fetchall()
print("\nThere are {} rows in the queried table.".format(len(texts)))

#initialize some useful objects
texts_list = [] #list of lists
keywords = set() #set of all words in all texts
j = len(texts) #number of documents

#can play with these bound parameters,
#which tell us which keywords are too rare or too common to consider
wordfreq_upperbound = 0.2*j
wordfreq_lowerbound = 0.045*j

tokenizer = RegexpTokenizer('\w+') #pick out alphanumeric sequences; discard punctuation, white space

progress = 0
for text in texts:
    #use tokenizer to clean list of words: remove punctuation, decapitalize
    text_words = [item.rstrip('\n').lower() for item in tokenizer.tokenize(text[0])] #each text is a list of words from tuple
    texts_list = texts_list + [text_words]
    keywords = keywords.union(set(text_words))
    if(progress % 100 == 0):
        print("Tokenized Text Bodies: {}. \n Keyword Count: {}.".format(progress, len(keywords)))
    progress = progress + 1
print("Done Tokenizing Words!")


#initialize more objects
keywords_index = list(keywords) #list of strings of keywords
correlation_matrix = np.zeros((len(keywords_index),j)) #matrix of keywords vs documents
col, row = 0, 0
print("Created an empty correlation matrix.")

matrixProg = 0
#ONE: create the correlation matrix
for text in texts_list:
    start = time.time()
    col = texts_list.index(text)
    for word in text:
        row = keywords_index.index(word)
        correlation_matrix[(row, col)]+=1
    end = time.time()
    if(matrixProg % 10 == 0):
        print("Text Bodies Processed: {}. Time Required: {}.\n".format(matrixProg, end-start))
    matrixProg = matrixProg + 1

#print stats from the correlation matrix without any keywords removed
print(correlation_matrix.shape)
print("average # of keywords per doc: " + str(correlation_matrix.sum(axis=0).sum(axis=0)/j))
print("average # of docs per keyword (with multiplicity): " + str(correlation_matrix.sum(axis=0).sum(axis=0)/correlation_matrix.shape[0]))


#TWO: make new_corr_matrix and new_keywords_index of words
#that aren't too common or too rare
i=0
new_corr_list = []
new_keywords_index = []
for row in correlation_matrix:
    row_list = list(row)
    word_freq = len(list(filter(lambda a: a != 0, row_list)))
    if word_freq < wordfreq_upperbound and word_freq > wordfreq_lowerbound:
        new_corr_list = new_corr_list + [row_list]
        new_keywords_index = new_keywords_index + [keywords_index[i]]
    i+=1

new_corr_matrix = np.array(new_corr_list)
	
#print stats from the corr matrix after removing words
print("--------------")
print(new_corr_matrix.shape)
print("average # of keywords per doc: " + str(new_corr_matrix.sum(axis=0).sum(axis=0)/j))
print("average # of docs per keyword (with multiplicity): " + str(new_corr_matrix.sum(axis=0).sum(axis=0)/new_corr_matrix.shape[0]))


#THREE: Analyze the rows of correlation_matrix:
#find related words (possible phrases) by computing the distance between 2 rows of the corr matrix
k=1
num_rows = new_corr_matrix.shape[0]
pairs = []
cutoff=2.8 #raising the cutoff above 3.4, we start to see phrases involving prepositions
for i in range(num_rows):
    for j in range(num_rows - i-1):
    	#compute the Euclidean distance between 2 rows
    	if np.linalg.norm(new_corr_matrix[i] - new_corr_matrix[i+j+1]) < cutoff:
    	    pairs = pairs + [new_keywords_index[i] + ' ' + new_keywords_index[i+j+1]]

#print the related words/pairs
#In our example, we didn't do much better than nltk methods 
#or parsing by looking at prepositional phrases.
#Possible benefits of this method: don't have to look for common prepositional structures by hand;
#good for finding related themes, but other methods were better for actually sorting documents
for pair in pairs:
    print(pair)
print(len(pairs))

#FOUR: Analyze the columns of correlation_matrix:

#method 1: find optimal hyperplanes that separate the groups of column vectors
#find the diameter of the column vectors

#method 2: k-means
#1. use k-means to group row vectors into keyword groups
#1b. merge keywords into keyword-groups (maybe by taking the average count of all keywords in a group as features for documents?)
#2. use k-means to group columns

#grouping column vectors (i.e., documents)
k=7 #number of document centroids, can play with this parameter
new_corr_matrix_t = np.transpose(new_corr_matrix) #k-means works on rows


#kmeans seems to give very disparate results
iterations = 10 #number of times to run kmeans; can change
group_counts = [0]*6

classifier = KMeans(n_clusters=8, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)
classifier.fit(new_corr_matrix_t)
keyword_centroids = classifier.cluster_centers_
# for j in range(iterations):
#     keyword_centroids = kmeans2(new_corr_matrix_t,k, minit='points')
#     #print keyword_centroids #prints [list of centroids, list of centroid assignments]

#     assignments = keyword_centroids[1].tolist()
#     for i in range(6):
#         group_counts[i] = assignments.count(i)
#     print(sorted(group_counts), sum(group_counts), keyword_centroids[0]) #prints number of documents per group, and the total number of docs grouped

print("kmeans ran")
smallest = 999999999
for i in range(7):
    center = keyword_centroids[i]
    center_array = np.array(center)
    for next_center in keyword_centroids[i+1:]:
        next_center_array = np.array(next_center)
        distance = np.linalg.norm(center_array - next_center_array)
        if distance < smallest:
            smallest = distance

print("found a smallest diameter")
largest = 0
for row in new_corr_matrix_t:
    centroid = np.array(keyword_centroids[classifier.predict(row)])
    distance = np.linalg.norm(centroid - row)
    if distance > largest:
        largest = distance

print("found a largest diameter")

if largest < smallest/3: 
    print("We had a good run of kmeans")



#Other matters:
#Can we use documents with lots of rare words to identify documents with lots of misspellings?
#Problems of scale involving sparse matrices--use scikit (ubuntu/virtual env issues), SVMs?


