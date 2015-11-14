#We apply ideas from ch 3 of Programming Collective Intelligence to titles from documents in city hall monitor.
#Namely, we construct the correlation matrix of keywords vs documents and see what that can teach us about organizing/grouping the documents.

import csv, collections
import numpy as np
from numpy import linalg
from nltk.tokenize import RegexpTokenizer
from scipy.cluster.vq import vq, kmeans2, whiten

#read in and preprocess the titles
input_file = open("data/communication_titles_01.csv", "rb")
titles = [row[0] for row in csv.reader(input_file)] #list of strings of titles

#initialize some useful objects
titles_list = [] #list of lists
keywords = set() #set of all words in all titles
j = len(titles) #number of documents

#can play with these bound parameters,
#which tell us which keywords are too rare or too common to consider
wordfreq_upperbound = 0.2*j
wordfreq_lowerbound = 0.045*j

tokenizer = RegexpTokenizer('\w+') #pick out alphanumeric sequences; discard punctuation, white space

for title in titles:
    #use tokenizer to clean list of words: remove punctuation, decapitalize
    title_words = map(str.lower,tokenizer.tokenize(title)) #each title is a list of words
    titles_list = titles_list + [title_words]
    keywords = keywords.union(set(title_words))

#initialize more objects
keywords_index = list(keywords) #list of strings of keywords
correlation_matrix = np.zeros((len(keywords_index),j)) #matrix of keywords vs documents
col, row = 0, 0

#ONE: create the correlation matrix
for title in titles_list:
    col = titles_list.index(title)
    for word in title:
	row = keywords_index.index(word)
	correlation_matrix[(row, col)]+=1

#print stats from the correlation matrix without any keywords removed
print correlation_matrix.shape
print "average # of keywords per doc: " + str(correlation_matrix.sum(axis=0).sum(axis=0)/j)
print "average # of docs per keyword (with multiplicity): " + str(correlation_matrix.sum(axis=0).sum(axis=0)/correlation_matrix.shape[0])


#TWO: make new_corr_matrix and new_keywords_index of words
#that aren't too common or too rare
i=0
new_corr_list = []
new_keywords_index = []
for row in correlation_matrix:
    row_list = list(row)
    word_freq = len(filter(lambda a: a != 0, row_list))
    if word_freq < wordfreq_upperbound and word_freq > wordfreq_lowerbound:
	new_corr_list = new_corr_list + [row_list]
	new_keywords_index = new_keywords_index + [keywords_index[i]]
    i+=1

new_corr_matrix = np.array(new_corr_list)
	
#print stats from the corr matrix after removing words
print "--------------"
print new_corr_matrix.shape
print "average # of keywords per doc: " + str(new_corr_matrix.sum(axis=0).sum(axis=0)/j)
print "average # of docs per keyword (with multiplicity): " + str(new_corr_matrix.sum(axis=0).sum(axis=0)/new_corr_matrix.shape[0])


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
    print pair
print len(pairs)

#FOUR: Analyze the columns of correlation_matrix:

#method 1: find optimal hyperplanes that separate the groups of column vectors
#find the diameter of the column vectors

#method 2: k-means
#1. use k-means to group row vectors into keyword groups
#1b. merge keywords into keyword-groups (maybe by taking the average count of all keywords in a group as features for documents?)
#2. use k-means to group columns

#grouping row vectors
k=7 #number of keyword centroids, can play with this parameter
white_corr_matrix = whiten(new_corr_matrix)
keyword_centroids = kmeans2(new_how_matrix,k)
print keyword_centroids #how to get cluster assigments: try pycluster or python-cluster instead?


#Other matters:
#Can we use documents with lots of rare words to identify documents with lots of misspellings?
#Problems of scale involving sparse matrices--use scikit (ubuntu/virtual env issues), SVMs?


