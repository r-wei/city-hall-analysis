import os
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer
import numpy as np
from numpy import linalg

#make a new corpus
corpusdir = 'communications/' #where the files are
newcorpus = PlaintextCorpusReader(corpusdir, '.*')

fileids = newcorpus.fileids() #list of fileids
j = len(fileids) #number of docs

files_text = [] #list of lists of words
tokenizer = RegexpTokenizer('\w+') #pick out alphanumeric sequences; discard punctuation, white space
keywords = set() #set of keywords

#create set of keywords and list of file texts
for id in fileids:
    raw = newcorpus.raw(id)
    raw2 = ''.join([i if ord(i)<128 else '' for i in raw]) #remove unicode characters
    raw3 = raw2.encode('ascii')
    file_words = map(str.lower,tokenizer.tokenize(raw3)) #list of cleaned words: lower-case, no punct, no whitespace
    files_text.append(file_words)
    keywords = keywords.union(set(file_words))

#initialize more objects
keywords_index = list(keywords) #list of strings of keywords
correlation_matrix = np.zeros((len(keywords_index),j)) #matrix of keywords vs documents
row = 0

#ONE: create the correlation matrix
for col in range(j):
    for word in files_text[col]:
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

#can play with these bound parameters,
#pick out the rare words
wordfreq_upperbound = 0.005*j
wordfreq_lowerbound = 0*j

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

