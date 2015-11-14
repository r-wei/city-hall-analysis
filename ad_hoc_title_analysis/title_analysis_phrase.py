#This analysis supposes that thematic part of a document is contained in the first phrase of its title. We truncate each title by either (1)l picking off everything preceding a prepositional phrase starting with 'for' or preceding an identifying number, or by (2) cutting off the end prepositional phrases starting with 'at or 'as'.

#This algorithm was tailored to the ORDINANCES matter_type, but worked well for CLAIMS, too.

#We print statistics related to grouping documents according to their truncated titles. We also print a list of common truncated titles for further analysis. As usual, we list the tunable parameters first.


import csv, re, collections

#can play with these parameters
n = 4 #fallback: if all else fails, truncate a title to its first 4 words
k = 20 #print the top k most common truncated titles

#print everything to this file
output_file = open('test_results/title_stats5', 'w')

#read in and preprocess the titles
input_file = open("data/claim_titles_01.csv", "rb")
titles = [row[0] for row in csv.reader(input_file)] #list of strings of titles

titles_trunc = [] #will be a list of strings

#Algorithm: For each title,
#1) find the first instance of either ' for '  or ' No. ', and truncate
#2) else, find the last instance of either ' at ' or ' as ', and truncate
#3) else, truncate after n=4 words

first_inst_pattern = re.compile(r"(.+?)( for | No\. )(.*)")
last_inst_pattern = re.compile(r"(.+)( at | as )(.*)")

for title in titles:
  match = first_inst_pattern.match(title)
  if match != None:
    titles_trunc = titles_trunc + [match.group(1)]
  else:
    match = last_inst_pattern.match(title)
    if match != None:
      titles_trunc = titles_trunc + [match.group(1)]
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
