import difflib 
import os
import csv
import nltk
from pprint import pprint
from nltk import metrics, stem, tokenize, data

# This section of code defines a method for matching strings that are not 
# exactly the same, but pretty similar.
stemmer = stem.PorterStemmer()
def normalize(s):
    words = tokenize.wordpunct_tokenize(s.lower().strip())
    return ' '.join([stemmer.stem(w) for w in words])
 
def fuzzy_match(s1, s2, max_dist=2):
    return metrics.edit_distance(normalize(s1), normalize(s2)) <= max_dist

#Get a list of all the files
listFiles = os.listdir("docs")

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

#Open and read specific files
# zoningDoc = open('zoning/zoning.txt', "rb").read().splitlines()
# doc1 = open('zoning/'+listFiles[8], "rb").read().splitlines()
# doc2 = open('zoning/'+listFiles[9], "rb").read().splitlines()
# doc3 = open('zoning/'+listFiles[10], "rb").read().splitlines()
# doc4 = open('zoning/'+listFiles[11], "rb").read().splitlines()
# allDocs = [doc1, doc2, doc3]


meetingDates = ["Meeting Date"]+["N/A"]*len(listFiles)
status = ["Status"]+["N/A"]*len(listFiles)
sponsors = ["Sponsor(s)"]+["N/A"]*len(listFiles)
matterType = ["Matter Type"]+["N/A"]*len(listFiles)
title = ["Title"]+["N/A"]*len(listFiles)
committee = ["Committee"]+["N/A"]*len(listFiles)
section1 = ["Section 1"]+["N/A"]*len(listFiles)
section2 = ["Section 2"]+["N/A"]*len(listFiles)

count = 1

for docFile in listFiles: 
	#Open and read the document
	doc = open('docs/'+docFile, "r").read().splitlines()

	#Remove empty lines from the document list.
	doc = list(filter(None, doc))

	try:
	    doc.remove(' ')
	    doc.remove('')
	except ValueError:
	    pass

	section1Start = None;
	section2Start = None;

	
	for i in range(0, len(doc)):
		# doc[i] represents a line in the document
		if(fuzzy_match(doc[i], "Meeting Date:")):
			# If you find a Meeting Date, append the next line 
			# which should be the actual date.
			meetingDates[count] = doc[i+1]
		elif(fuzzy_match(doc[i], "Status:")):
			status[count] = doc[i+1]
		elif(fuzzy_match(doc[i], "Sponsor(s):")):
			sponsors[count] = doc[i+1]
		elif(fuzzy_match(doc[i], "Type:")):
			matterType[count] = doc[i+1]
		elif(fuzzy_match(doc[i], "Title:")):
			title[count] = doc[i+1]
		elif(fuzzy_match(doc[i], "Committee(s) Assignment:")):
			committee[count] = doc[i+1]
		if("section 1." in doc[i].lower()):
			section1Start = i
		if("section 2." in doc[i].lower()):
			section2Start = i

	# Grab the Section 1 
	s1 = doc[section1Start:section2Start]
	s1 = " ".join(s1)
	section1[count] = s1

	# Grab Section 2
	s2 = doc[section2Start:]
	s2 = " ".join(s2)
	s2 = tokenizer.tokenize(s2)
	
	# This breaks Section 2 into it's individual sentences
	# and then takes the primary sentence of that section
	section2[count] = s2[1];


	count = count+1;

	
#This section ties together information for the same document across different lists.
allLists = [meetingDates, status, sponsors, matterType, title, committee, section1, section2]
allLists = list(zip(*allLists))

csvName = 'zoning.csv'
with open(csvName, 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	for row in allLists:
		writer.writerow(row);

print("Reduced Zoning documents to structured data and stored in {}".format(csvName))