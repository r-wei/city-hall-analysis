from __future__ import print_function

import sys
from time import time

import psycopg2

from analyze_titles import *
from compileDicts import * 
import collections

import os

###############################################################################

#Function for clearly printing a dictionary's values
def dictPrint(dictIn):
  try: 
    for attribute, value in dictIn.items():
      print('{} : {}'.format(attribute, value))
    print('\n')
  except:
    f1.write('\n =============================== \n PRINTING ISSUE \n =============================== \n')

###############################################################################

print("loading city hall monitor documents")

documents = []
titles = []

############ Connect to the database
try:
    conn = psycopg2.connect(database='cityhallmonitor',user='cityhallmonitor',password='cityhallmonitor',host='localhost')
           #psycopg2.connect("dbname='cityhallmonitor' user='Bomani' host='localhost' password='wolfbite1'")
    print("Database Connected!")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()
t0 = time()
cur.execute('select matter_attachment_id, title, text from cityhallmonitor_document')
#cur.execute('select matter_attachment_id, title, text from cityhallmonitor_matter m , cityhallmonitor_matterattachment ma , cityhallmonitor_document d where m.id=ma.matter_id and ma.id=d.matter_attachment_id')

############ Format data: make a dictionary of keys:values = matter_id:(title, text)
documentDict = {}
for row in cur:
  documentDict[row[0]] = (row[1], row[2])

print("%d documents" % len(documentDict.keys()))
print()
print("done in %fs" % (time() - t0))

############# Machine analyze: Run title analysis 3 times
groupedDicts = [dict()]
remainingDicts = [documentDict]

for i in range(3):
	analyzed = title_analysis(remainingDicts[i])
	groupedDicts.append(analyzed[0])
	remainingDicts.append(analyzed[1])

#print results of each title analysis
for dic in groupedDicts:
	dictPrint(getIndex(dic))

############ Display results: merge results from 3 iterations of title analysis by hand,
############ and print out groups of truncated titles
result = compileDictionaries(groupedDicts[1], groupedDicts[2], groupedDicts[3])
dictPrint(getIndex(result))


