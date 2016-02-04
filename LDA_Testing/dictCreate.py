import csv, collections
import numpy as np
from numpy import linalg
from nltk.tokenize import RegexpTokenizer

#read in and preprocess the titles
input_file = open("restoftitles.csv", "rb")
# titles = [row[0] for row in csv.reader(input_file)] #list of strings of titles

titles = []
with open('restoftitles.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for line in reader:
		if(len(line) > 0):
			titles.append(line[0])

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

no_nums = [x for x in keywords if not x.isdigit()]

# Write word to file
filename = 'dictnostops.txt'
file_ = open(filename, 'w')
for word in no_nums:
	file_.write(word+'\n')
file_.close()


# import csv
# import nltk.tokenize import RegexpTokenizer

# titleWords = []
# titles
# with open('restoftitles.csv','rb') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',')
# 	filename = 'dictnostops.txt'
# 	file_ = open(filename, 'w')
# 	for line in reader:

# 		# print(line)
# 		# if(len(line) > 0):
# 		# 	t = line[0]
# 		# 	words = t.split()
# 		# 	for w in words:
# 		# 		titleWords.append(w)
				
	

# uniqueWords = list(set(titleWords))

# # Write word to file
# for word in uniqueWords:
# 	file_.write(word+'\n')
# file_.close()
	




		
