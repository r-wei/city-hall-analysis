#analyze all titles, truncating with phrases
#see parsers.py for the truncating algorithm

import csv, re, collections
from parsers import *

#can play with these parameters
k = 100 #print the top k most common truncated titles
k2 = 30 #throw everything except those grouped in the top k2 truncated titles back in for analysis

#print everything to these files
output_file = open('test_results/title_stats5', 'w')
new_csv = open('remainingTitles.csv', 'w')
new_csv2 = open('throwbackTitles.csv', 'w')

#read in the titles
input_file = open("allTitles.csv", "rb")
titles = [row[0] for row in csv.reader(input_file)] #list of strings of titles

titles_trunc = [] #will be a list of strings
remaining_titles = [] #list of strings
grouped_titles = [] #list of tuples (full title, trunc title)
strategies = [ordinance_parser] #parsing strategies; only one so far

#apply the parsing strategies to each title
for row in titles:
    result = apply_strategies(row, strategies)
    if result != None: 
	titles_trunc = titles_trunc + [result]
	grouped_titles = grouped_titles + [(row,result)]
    else:
	remaining_titles = remaining_titles + [row]

#write the remaining (unorganized titles) to a new csv file
#there are no remaining_titles right now because the parsers group all the titles 
#(if all else fails, truncate after 4 words)
for row in remaining_titles:
    new_csv.write("%s\n" % row)

#print the strategies used
line = "Strategies used: " + str(strategies)
output_file.write("%s\m" % line)

#total number of docs we've organized
line = "Number of docs organized by these strategies: " + str(len(titles_trunc))
output_file.write("%s\m" % line)

#count how often each truncated title occurs
#create a dictionary of (title_trunc, #occurences) pairs
counter = collections.Counter(titles_trunc)

#print the number of groups
line = "Number of groups organized by these strategies is: "+ str(len(counter))
output_file.write("%s\n" % line)

#compute and print the total number of titles included in the top k most common
top_k = counter.most_common(k)
sum = 0
for top in top_k:
    sum += top[1]

line = "Total number of documents within the top " + str(k) + " most common titles: " + str(sum)
output_file.write("%s\n" % line)
output_file.write("\n\n")

#print the top k most common titles
for item in top_k:
    output_file.write("%s\n" % str(item))

#if a row is not grouped in the top_k most common titles, add it to throwback_titles for further ainalysis
#if a row starts with 'Call ', also put it it in remaining_titles (we know this group is not well-formed)
top_k2 = counter.most_common(k2)
test = False
for title,trunc in grouped_titles:
    if title.startswith('Call ') == False:
    	for top in top_k2:
            if trunc == top[0]:
	    	test = True
	   	break
    if test == False:
	new_csv2.write("%s\n" % title)
    test = False

