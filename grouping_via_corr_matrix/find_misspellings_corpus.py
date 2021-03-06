#Tried to find misspellings in a corpus of text files. See find_misspellings.py and grouping_docs.py for documentation.
#There are ~30,400 unique words in these 49 communication files
#Rebecca's laptop took too long to make the correlation matrix

import os
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer
import numpy as np
from numpy import linalg

#make a new corpus
corpusdir = 'communications/small_test_batch' #where the files are
newcorpus = PlaintextCorpusReader(corpusdir, '.*')

fileids = newcorpus.fileids() #list of fileids
j = len(fileids) #number of docs

words_list = [] #['doc', '1', 'words', 'doc', '2', 'words',...]
doc_breaks = [0] #ith entry = index of first word in doc i in words_list
keywords = set() #{'doc', '1', 'words', '2',...}

tokenizer = RegexpTokenizer('\w+') #pick out alphanumeric sequences; discard punctuation, white space

#create set of keywords and list of file texts
for id in fileids:
    raw = newcorpus.raw(id)
    raw2 = ''.join([i if ord(i)<128 else '' for i in raw]) #remove unicode characters
    raw3 = raw2.encode('ascii')
    file_words = map(str.lower,tokenizer.tokenize(raw3)) #list of cleaned words: lower-case, no punct, no whitespace
    words_list = words_list + file_words
    doc_breaks = doc_breaks + [len(file_words)+doc_breaks[len(doc_breaks)-1]]
    
doc_breaks = doc_breaks + [len(words_list)]
keywords = set(words_list)
print 'Number of keywords: ' + str(len(keywords))
print 'Number of total words: ' + str(len(words_list))

red_keywords = set() #reduced set of keywords; try to remove too common words to save matrix computation later
cutoff = 3*j

sorted_words_list = sorted(words_list)
flipped_words_list = sorted_words_list[::-1]
print "Done sorting and flipping."

L = len(sorted_words_list) - 1
for word in keywords:
    start = sorted_words_list.index(word)
    stop = L - flipped_words_list.index(word)
    if stop - start < cutoff:
	red_keywords = red_keywords.union({word})
	#print word, n

print 'Number of reduced keywords: ' + str(len(red_keywords))

#initialize more objects
keywords_index = list(red_keywords) #list of strings of keywords
correlation_matrix = np.zeros((len(keywords_index),j)) #matrix of keywords vs documents
row = 0

#ONE: create the correlation matrix
for doc in range(j):
    for word in words_list[doc_breaks[doc]:doc_breaks[doc+1]]:
	try:
    	    row = keywords_index.index(word)
	    correlation_matrix[(row, doc)]+=1
	except ValueError:
	    pass
	

#print stats from the correlation matrix without any keywords removed
print correlation_matrix.shape
print "average # of keywords per doc: " + str(correlation_matrix.sum(axis=0).sum(axis=0)/j)
print "average # of docs per keyword (with multiplicity): " + str(correlation_matrix.sum(axis=0).sum(axis=0)/correlation_matrix.shape[0])

#TWO: separate the correlation_matrix and keywords_index into
#rare vs common corr_matrix and keywords_index, resp.
i=0
rare_corr_list = []
common_corr_list = []
rare_keywords_index = []
common_keywords_index = []

#can play with these bound parameters,
#pick out the rare words
wordfreq_upperbound = 0.11*j
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
print "average # of docs per rare word (with multiplicity): " + str(rare_corr_matrix.sum(axis=0).sum(axis=0)/rare_corr_matrix.shape[0])

