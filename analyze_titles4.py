import csv, re, collections

#print everything to this file
output_file = open('test_results/title_stats4', 'w')

#read in and preprocess the titles
input_file = open("data/ordinance_titles_01.csv", "rb")
titles = [row[0] for row in csv.reader(input_file)] #list of strings of titles

titles_trunc = [] #will be a list of strings

#can play with these variables
n = 4
k = 20

#Algorithm: For each title,
#1) find the first instance of ' for ' and truncate
#2) else, find the first instance of ' No. ' and truncate
#3) else, find the last instance of ' at ' and truncate
#4) else, find the last instance of ' as ' and truncate
#4) else, truncate after n=4 words
for title in titles:
    j = title.find(' for ')
    if j > -1:
	titles_trunc = titles_trunc + [title[:j]]
    else:
	j = title.find(' No. ')
	if j > -1:
	    titles_trunc = titles_trunc + [title[:j]]
	else:
	    j = title.rfind(' at ')
	    if j > -1:
	    	titles_trunc = titles_trunc + [title[:j]]
	    else:
		j = title.rfind(' as ')
	    	if j > -1:
	    	    titles_trunc = titles_trunc + [title[:j]]
	   	else:
		    title_split = title.split(' ') #each title is a list of strings of words
	            m = min(n, len(title))
        	    title_trunc = ' '.join(title_split[:m])
	
        	    titles_trunc = titles_trunc + [title_trunc] 

#count how often each truncated title occurs
#create a dictionary of (title_trunc, #occurences) pairs
counter = collections.Counter(titles_trunc)

#print the number of groups given by truncating titles to length n
line = "Number of groups given by this grouping algorithm is: "+ str(len(counter))
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
