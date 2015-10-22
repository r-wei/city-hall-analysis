#try to find misspellings using rare words identified by the correlation matrix
#note: here, rare words = keywords

import csv, collections
import numpy as np
from numpy import linalg

#read in and preprocess the titles
input_file = open("data/communication_titles_01.csv", "rb")
titles = [row[0] for row in csv.reader(input_file)] #list of strings of titles

#initialize some useful objects
titles_list = [] #list of lists
keywords = set() #set of all words in all titles
j = len(titles) #number of documents

#can play with these bound parameters,
#pick out the rare words
wordfreq_upperbound = 0.005*j
wordfreq_lowerbound = 0*j

for title in titles:
    title_words = title.split(' ') #each title is a list of strings of words
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
print "average # of docs per keyword: " + str(correlation_matrix.sum(axis=0).sum(axis=0)/correlation_matrix.shape[0])


#TWO: make new_corr_matrix and new_keywords_index of rare words
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
#these stats are not so promising--there appear to be a lot of rare words
print "--------------"
print new_corr_matrix.shape
print "average # of rare words per doc: " + str(new_corr_matrix.sum(axis=0).sum(axis=0)/j)
print "average # of docs per rare word: " + str(new_corr_matrix.sum(axis=0).sum(axis=0)/new_corr_matrix.shape[0])

#THREE: find a document with lots of rare words
cutoff=3
potential_docs = []

num_rare_words = new_corr_matrix.sum(axis=0)
for i in range(j):
    if num_rare_words[i] > cutoff:
	potential_docs = potential_docs + [titles[i]]

print len(potential_docs)



