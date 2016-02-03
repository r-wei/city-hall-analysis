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

		elif(dict2[key][4] != 0 and dict2[key][4] != 4 and dict2[key][4] != -1):
			newIndex = dict2[key][4]+16
			tup = dict2[key][:4] +  (newIndex,) 
			dict1[key] = tup

	for key in keys3:
		if(dict3[key][4] == 3):
			tup = dict3[key][:4] +  (3,) 
			dict1[key] = tup
		elif(dict3[key][4] == 10):
			tup = dict3[key][:4] +  (1,) 
			dict1[key] = tup
		elif(dict3[key][4] == 12):
			tup = dict3[key][:4] +  (15,) 
			dict1[key] = tup
		elif(dict3[key][4] == 15):
			tup = dict3[key][:4] +  (31,) 
			dict1[key] = tup
		elif(dict3[key][4] != -1):
			newIndex = dict3[key][4]+33
			tup = dict3[key][:4] +  (newIndex,) 
			dict1[key] = tup

	keys1 = dict1.keys()
	for key in keys1:
		if(dict1[key][4] in [0,2,4,9,11]):
			tup = dict1[key][:4] +  (0,)
			dict1[key] = tup
		elif(dict1[key][4] in [1, 12]):
			tup = dict1[key][:4] +  (1,)
			dict1[key] = tup
		elif(dict1[key][4] in [10,13,22,30,32,35,38]):
			tup = dict1[key][:4] +  (2,)
			dict1[key] = tup
		elif(dict1[key][4] in [5,15,16,21,29,40,33,42,44]):
			tup = dict1[key][:4] +  (3,)
			dict1[key] = tup
		elif(dict1[key][4] in [6,8,19]):
			tup = dict1[key][:4] +  (4,)
			dict1[key] = tup
		elif(dict1[key][4] in [3,14,31,47,49]):
			tup = dict1[key][:4] +  (5,)
			dict1[key] = tup
		elif(dict1[key][4] in [7,18]):
			tup = dict1[key][:4] +  (6,)
			dict1[key] = tup
		elif(dict1[key][4] in [26,46]):
			tup = dict1[key][:4] +  (7,)
			dict1[key] = tup
		elif(dict1[key][4] in [34,37,39]):
			tup = dict1[key][:4] +  (8,)
			dict1[key] = tup
				

	#dict_index[integer index] = set of truncated titles with this index
	dict_index = dict()
	for key in dict1.keys():
		trunc = dict1[key][2]
		index = dict1[key][4]
		if index != -1:
			if index in dict_index.keys():
				dict_index[index] = dict_index[index].union({trunc})
			else:
				dict_index[index] = {trunc}

	return(dict1, dict_index)




