#baby version of title_analysis_trunc
#see title_analysis_trunc for documentation

import csv, re, collections

input_file = open("data/ordinance_titles_01.csv", "rb")
titles = [row[0] for row in csv.reader(input_file)] #list of titles
titles_trunc = []

#truncate each title to the first four words
#return a list of truncated strings
for title in titles:
    title_trunc = re.findall(r"(.*?)\s(.*?)\s(.*?)\s(.*?)\s",title)
    if len(title_trunc) == 0:
	titles_trunc = titles_trunc + [title]
	
    else:
	title_str = ' '.join(list(title_trunc[0]))
	titles_trunc = titles_trunc + [title_str]

#count how often each truncated title occurs
#create a dictionary of (title_trunc, #occurences) pairs
counter=collections.Counter(titles_trunc)
print counter
