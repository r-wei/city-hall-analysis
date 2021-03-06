#attempt to organize matter_dump by matter_type

import csv, re, collections

input_file = open("data/matter_dump.csv", "rb")
rows = [row for row in csv.reader(input_file)] #list of titles


remove_known = []
new_ids = []

for row in rows:
    if row[2] != '53': #these are ordinances
	if row[2] != '66': #these are claims
	    remove_known = remove_known + [row]
	    new_ids = new_ids + [row[2]]


#counter=collections.Counter(new_ids)
#print counter

names_61, names_55, names_52 = [], [], []

for row in remove_known:
    if row[2] == '61': #these have names similar to ordinances
	names_61 = names_61 + [row[0]]
    elif row[2] == '55': #these are probably appointments
	names_55 = names_55 + [row[0]]
    elif row[2] == '52': #these are probably resolutions
	names_52 = names_52 + [row[0]]

counter=collections.Counter(names_52)
print counter

