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
		elif(dict3[key][4] == 11):
			tup = dict3[key][:4] +  (12,) 
			dict1[key] = tup
		elif(dict3[key][4] == 12):
			tup = dict3[key][:4] +  (15,) 
			dict1[key] = tup
		elif(dict3[key][4] == 15):
			tup = dict3[key][:4] +  (31,) 
			dict1[key] = tup
		elif(dict3[key][4] != -1):
			newIndex = dict3[key][4]+32
			tup = dict3[key][:4] +  (newIndex,) 
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




