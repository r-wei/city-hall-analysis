import collections

def compileDictionaries(dict1, dict2, dict3):
	
	###### For Dict2 Processing... ######
	#Get keys from each dict
	keys1 = dict1.keys()
	keys2 = dict2.keys()
	keys3 = dict3.keys()

	for key in keys2:
		#Moving Amendments of Municipal Code
		if(dict2[key][4] == 1):
			tup = dict2[key][:4] +  (0,) 
			dict1[key] = tup

		elif(dict2[key][4] == 7 or dict2[key][4] == 11):
			tup = dict2[key][:4] +  (8,) 
			dict1[key] = tup

		elif(dict2[key][4] == 9):
			tup = dict2[key][:4] +  (1,) 
			dict1[key] = tup

		elif(dict2[key][4] != 0 and dict2[key][4] != 4):
			newIndex = dict2[key][4]+16
			tup = dict2[key][:4] +  (newIndex,) 
			dict1[key] = tup

	trunc_titles = []
	indices = []
	for key in dict1.keys():
		trunc_titles.append(dict1[key][2])
		indices.append(dict1[key][4])

	print(collections.Counter(trunc_titles))
	print(collections.Counter(indices))


	return(dict1)




