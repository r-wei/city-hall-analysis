#We apply ideas from ch 3 of Programming Collective Intelligence
#to titles from documents in city hall monitor.
#Namely, we construct the correlation matrix of keywords vs documents
#and see what that can teach us about organizing/grouping the documents.

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
#which tell us which keywords are too rare or too common to consider
wordfreq_upperbound = 0.2*j
wordfreq_lowerbound = 0.045*j

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


#TWO: delete the rows of keywords that are too common or too rare in the correlation_matrix
#also delete the keywords from keywords_index
i=0
for row in correlation_matrix:
    row_list = list(row)
    word_freq = len(filter(lambda a: a != 0, row_list))
    if word_freq > wordfreq_upperbound or word_freq < wordfreq_lowerbound:
	correlation_matrix = np.delete(correlation_matrix, i, axis=0)
	keywords_index.remove(keywords_index[i])
    else:
	#print keywords_index[i] #this prints the remaining keywords   
	i+=1
	
#print stats from the corr matrix after removing words
print "--------------"
print correlation_matrix.shape
print "average # of keywords per doc: " + str(correlation_matrix.sum(axis=0).sum(axis=0)/j)
print "average # of docs per keyword: " + str(correlation_matrix.sum(axis=0).sum(axis=0)/correlation_matrix.shape[0])


#THREE: find related words (possible phrases) by computing the distance between 2 rows of the corr matrix
k=1
num_rows = correlation_matrix.shape[0]
pairs = []
cutoff=3.4 #raising the cutoff above 3.4, we start to see phrases involving prepositions
for i in range(num_rows):
    for j in range(num_rows - i-1):
	#compute the Euclidean distance between 2 rows
	if np.linalg.norm(correlation_matrix[i] - correlation_matrix[i+j+1]) < cutoff:
	    pairs = pairs + [keywords_index[i] + ' ' + keywords_index[i+j+1]]

#print the related words/pairs
#In our example, we didn't do much better than nltk methods 
#or parsing by looking at prepositional phrases.
#Possible benefits of this method: don't have to look for common prepositional structures by hand;
#good for finding related themes, but other methods were better for actually sorting documents
for pair in pairs:
    print pair
print len(pairs)

#FOUR: classify documents by comparing columns of the matrix (to do!)
#try finding optimal hyperplanes that separate the groups?
#try k-means?

#Other matters:
#Can we use documents with lots of rare words to identify documents with lots of misspellings?
#Problems of scale involving sparse matrices--use scikit, SVMs?


