import csv, collections, string
import networkx as nx
import matplotlib.pyplot as plt

#initialize a graph
G = nx.Graph()

#print everything to this file
output_file = open('test_results/comm_stats', 'w')

#read in and preprocess the titles
input_file = open("data/communication_titles_01.csv", "r")
titles = [row[0] for row in csv.reader(input_file)] #list of strings of titles
titles_set = [] #will be a list of sets


for title in titles:  
    #title_nopunct = title.translate(string.maketrans("",""), string.punctuation) #remove punctuation
    title_nopunct = "".join(c for c in title if c not in ('!','.',':'))
    title_split = title_nopunct.split(' ') #each title is a list of strings of words
    title_split = [s.lower() for s in title_split] #lowercase
    title_split = set(title_split) - {'of', 'and', '', 'for', 'chicago'}
    titles_set = titles_set + [title_split]

threshhold = 5
count = [0]*209
title_number = 0
titles_after = []

for title1 in titles_set:
    # print "-----------------------------"
    #print title1
    #print "-----------------------------"
    G.add_node(title_number)
    titles_after = titles_set[title_number+1:]

    for title2 in titles_after:
        overlap = title1.intersection(title2)
        if len(overlap) > threshhold:
            #    print title2
            count[title_number] = count[title_number] + 1
            G.add_edge(title_number, titles_after.index(title2) + title_number + 1)
    title_number = title_number + 1

#print count

#counter = collections.Counter(count)
#print counter

pos = nx.spring_layout(G, scale=20)

nx.draw(G,pos)
plt.show()
