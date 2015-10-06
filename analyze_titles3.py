import csv, collections

#print everything to this file
output_file = open('title_stats3', 'w')

#read in and preprocess the titles
input_file = open("matter_titles_01.csv", "rb")
titles = [row[0] for row in csv.reader(input_file)] #list of strings of titles
titles_split = [] #will be a list of lists
titles_trunc = [] #will be a list of strings

for title in titles:
    title_split = title.split(' ') #each title is a list of strings of words
    titles_split = titles_split + [title_split]

#variables for totaling over all of the for loops
all_top_k = []
full_counter = collections.Counter()

#can play with these parameters
trunc_lengths = [4,3,2,1]
k = 20

for n in trunc_lengths:

    #truncate each title to n words
    #produce a list of strings of truncated titles
    titles_trunc = []
    for title in titles_split:
        m = min(n, len(title))
        title_trunc = ' '.join(title[:m])
	
        titles_trunc = titles_trunc + [title_trunc] 

    #count how often each truncated title occurs
    #create a dictionary of (title_trunc, #occurences) pairs
    counter_n = collections.Counter(titles_trunc)

    #print the number of groups given by truncating titles to length n
    line = "Number of groups given by truncating titles to " + str(n) + " words: "+ str(len(counter_n))
    output_file.write("%s\n" % line)

    #compute and print the total number of titles included in the top k most common of length n
    top_k = counter_n.most_common(k)
    sum = 0
    for top in top_k:
        sum += top[1]

    line = "Total number of documents within the top " + str(k) + " most common titles: " + str(sum)
    output_file.write("%s\n" % line)
    output_file.write("\n\n")

    #add counter_n to the full_counter
    full_counter = full_counter + counter_n

#print (more or less) the top k most common titles of all truncation lengths
all_top_k = full_counter.most_common(len(trunc_lengths)*k)
for item in all_top_k:
    output_file.write("%s\n" % str(item))
