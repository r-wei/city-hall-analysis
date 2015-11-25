from __future__ import print_function
from collections import defaultdict
import re
import sys
from time import time
import numpy as np
import operator
import csv, json


from sklearn.feature_extraction.text import TfidfVectorizer

# import plotly.plotly as py
# import plotly.graph_objs as go
# import json

corpus = []
amount = 50
start_gram = 1
end_gram = 3
minDf = 100

#Function for clearly printing a dictionary's values
def dictPrint(dictIn):
	for attribute, value in dictIn.items():
		print('{} : {}'.format(attribute, value))
	print('\n')

def getCorpus(cursor):
	count = 0
	with open('allTitles.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			corpus.append(row[0])


getCorpus(corpus)

vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(start_gram, end_gram), min_df = minDf, stop_words = 'english', use_idf='True')
X = vectorizer.fit_transform(corpus)
idf = vectorizer.idf_
zipped = dict(zip(vectorizer.get_feature_names(), idf))
sorted_dict = sorted(zipped.items(), key=operator.itemgetter(1), reverse=True)
json.dump(sorted_dict, open("topWords.txt",'w'))


with open("topWords.txt", 'w') as txtFile:
	txtFile.write('Top {} Terms: n-gram range {} to {} with min_df={}. Analyzed {} titles.\n'.format(amount, start_gram, end_gram, minDf, len(corpus)))
	txtFile.write('---------------------------------------------\n')
	for x in range(0,amount):
		outString  = '{} | {} \n'.format(sorted_dict[x][1], sorted_dict[x][0])
		txtFile.write(outString)
	


