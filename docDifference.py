import difflib 
import os
import csv
from pprint import pprint
from nltk import metrics, stem, tokenize

# This section of code defines a method for matching strings that are not 
# exactly the same, but pretty similar.
stemmer = stem.PorterStemmer()
def normalize(s):
    words = tokenize.wordpunct_tokenize(s.lower().strip())
    return ' '.join([stemmer.stem(w) for w in words])
 
def fuzzy_match(s1, s2, max_dist=2):
    return metrics.edit_distance(normalize(s1), normalize(s2)) <= max_dist

#Get a list of all the files
listFiles = os.listdir("zoning")

#Open and read the files
zoningDoc = open('zoning/zoning.txt', "rb").read().splitlines()
doc1 = open('zoning/'+listFiles[8], "rb").read().splitlines()
doc2 = open('zoning/'+listFiles[9], "rb").read().splitlines()
doc3 = open('zoning/'+listFiles[10], "rb").read().splitlines()
doc4 = open('zoning/'+listFiles[11], "rb").read().splitlines()



allDocs = [doc1, doc2, doc3]

meetingDates = []
status = []
sponsors = []
matterType = []
title = []
committee = []
for doc in allDocs: 
	#Remove empty lines from the document list.
	doc = list(filter(None, doc))
	doc.remove(' ')
	for i in range(0, len(doc)):
		# doc[i] represents a line in the document
		if(fuzzy_match(doc[i], "Meeting Date:")):
			# If you find a Meeting Date, append the next line 
			# which should be the actual date.
			meetingDates.append(doc[i+1])
		elif(fuzzy_match(doc[i], "Status:")):
			status.append(doc[i+1])
		elif(fuzzy_match(doc[i], "Sponsor(s):")):
			sponsors.append(doc[i+1])
		elif(fuzzy_match(doc[i], "Type:")):
			matterType.append(doc[i+1])
		elif(fuzzy_match(doc[i], "Title:")):
			title.append(doc[i+1])
		elif(fuzzy_match(doc[i], "Committee(s) Assignment:")):
			committee.append(doc[i+1])	

pprint(meetingDates)
pprint(status)
pprint(sponsors)
pprint(matterType)
pprint(title)
pprint(committee)

# with open('zoning/zoning.csv', 'wb') as csvfile:
#     writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)




# for doc in allDocs: 
# 	print(doc)
# 	d = difflib.Differ()
# 	diff = d.compare(zoningDoc, doc)
# 	result = list(diff)
# 	pprint(result)
# 	changes = []
# 	for line in result:
# 		firstChar = line[0]
# 		if(firstChar == '+'):
# 			if(line != ''):
# 				line = line[2:]				
# 				changes.append(line)
			

	#pprint(changes)

# s = difflib.SequenceMatcher(None, doc1, doc2)
# print(s)
# for block in s.get_matching_blocks():
# 	print("a[%d] and b[%d] match for %d elements" % block)

#print('\n'.join(diff))

# diff = difflib.ndiff(zoningDoc, doc1)
# print(diff)

# input_file = open("zoning/ordinance_titles_01.csv", "rb")
# d = difflib.Differ()
# diff = d.compare(text1_lines, text2_lines)
# print '\n'.join(diff)