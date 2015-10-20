import difflib 
import os
from pprint import pprint

#Get a list of all the files
listFiles = os.listdir("zoning")

#Open and read the files
zoningDoc = open('zoning/zoning.txt', "rb").read().decode("utf-8").splitlines()
doc1 = open('zoning/'+listFiles[8], "rb").read().decode("utf-8").splitlines()
doc2 = open('zoning/'+listFiles[9], "rb").read().decode("utf-8").splitlines()


# s = difflib.SequenceMatcher(None, doc1, doc2)
# print(s)
# for block in s.get_matching_blocks():
# 	print("a[%d] and b[%d] match for %d elements" % block)

d = difflib.Differ()
diff = d.compare(zoningDoc, doc2)
result = list(diff)
#print(result)
changes = []
for line in result:
	firstChar = line[0]
	if(firstChar == '+'):
		line = line[2:]
		changes.append(line)

pprint(changes)

#print('\n'.join(diff))

# diff = difflib.ndiff(zoningDoc, doc1)
# print(diff)

# input_file = open("zoning/ordinance_titles_01.csv", "rb")
# d = difflib.Differ()
# diff = d.compare(text1_lines, text2_lines)
# print '\n'.join(diff)