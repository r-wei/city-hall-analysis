#try to find misspellings using rare words identified by the correlation matrix
#note: here, rare words = keywords
#results weren't promising, even when we cleaned the words first 
#there are too many words that appear in only ONE title

import csv, collections
import numpy as np
from numpy import linalg
from nltk.tokenize import RegexpTokenizer

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
print "average # of docs per keyword: " + str(correlation_matrix.sum(axis=0).sum(axis=0)/correlation_matrix.shape[0])

#TWO: separate the correlation_matrix and keywords_index into
#rare vs common corr_matrix and keywords_index, resp.
i=0
rare_corr_list = []
common_corr_list = []
rare_keywords_index = []
common_keywords_index = []

for row in correlation_matrix:
    row_list = list(row)
    word_freq = len(filter(lambda a: a != 0, row_list))
    if word_freq < wordfreq_upperbound and word_freq > wordfreq_lowerbound:
	rare_corr_list = rare_corr_list + [row_list]
	rare_keywords_index = rare_keywords_index + [keywords_index[i]]
    else:
	common_corr_list = common_corr_list + [row_list]
	common_keywords_index = common_keywords_index + [keywords_index[i]]
    i+=1

rare_corr_matrix = np.array(rare_corr_list)
common_corr_matrix = np.array(common_corr_list)

	
#print stats about rare words
#these stats are not so promising--there appear to be a lot of rare words
print "--------------"
print rare_corr_matrix.shape
print "average # of rare words per doc: " + str(rare_corr_matrix.sum(axis=0).sum(axis=0)/j)
print "average # of docs per rare word: " + str(rare_corr_matrix.sum(axis=0).sum(axis=0)/rare_corr_matrix.shape[0])

#THREE: find a document with lots of rare words
#returns too many docs because there are too many rare words
cutoff=3
potential_docs = []

num_rare_words = rare_corr_matrix.sum(axis=0)
for i in range(j):
    if num_rare_words[i] > cutoff:
	potential_docs = potential_docs + [titles[i]]

print "number of docs with potentially many misspelled words: " + str(len(potential_docs))



