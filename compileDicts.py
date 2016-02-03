import collections

#####################
#Given a grouped dictionary, print out (index, truncated_title)
def getIndex(dict1):
	dict_index = dict()
	for key in dict1.keys():
		trunc = dict1[key][2]
		index = dict1[key][4]
		if index != -1:
			if index in dict_index.keys():
				dict_index[index] = dict_index[index].union({trunc})
			else:
				dict_index[index] = {trunc}

	return(dict_index)

################
#Merge results from 3 iterations of title analysis BY HAND
def compileDictionaries(dict1, dict2, dict3):
	keys1 = dict1.keys()
	keys2 = dict2.keys()
	keys3 = dict3.keys()


	for key in keys1:
		if(dict1[key][4] in [0,2,4,9,11]):
			tup = dict1[key][:4] +  (0,)#Public use
			dict1[key] = tup
		elif(dict1[key][4] in [1,12]):
			tup = dict1[key][:4] +  (1,)#Parking permits
			dict1[key] = tup
		elif(dict1[key][4] in [3,14]):
			tup = dict1[key][:4] +  (2,)#Claims, get money
			dict1[key] = tup
		elif(dict1[key][4] in [5,15,16]):
			tup = dict1[key][:4] +  (3,)#Traffic
			dict1[key] = tup
		elif(dict1[key][4] in [6,8]):
			tup = dict1[key][:4] +  (4,)#Recognition
			dict1[key] = tup
		elif(dict1[key][4] in [7]):
			tup = dict1[key][:4] +  (5,)#City development
			dict1[key] = tup
		elif(dict1[key][4] in [10,13]):
			tup = dict1[key][:4] +  (6,)#Exemptions
			dict1[key] = tup
	
	for key in keys2:
		if(dict2[key][4] in [1]):
			tup = dict2[key][:4] +  (0,)
			dict1[key] = tup
		elif(dict2[key][4] in [9]):
			tup = dict2[key][:4] +  (1,)
			dict1[key] = tup
		elif(dict2[key][4] in [15]):
			tup = dict2[key][:4] +  (2,)
			dict1[key] = tup
		elif(dict2[key][4] in [5,13]):
			tup = dict2[key][:4] +  (3,)
			dict1[key] = tup
		elif(dict2[key][4] in [3,7,11]):
			tup = dict2[key][:4] +  (4,)
			dict1[key] = tup
		elif(dict2[key][4] in [2]):
			tup = dict2[key][:4] +  (5,)
			dict1[key] = tup
		elif(dict2[key][4] in [6,14,16]):
			tup = dict2[key][:4] +  (6,)
			dict1[key] = tup
		elif(dict2[key][4] in [10]):
			tup = dict2[key][:4] +  (7,)#Permits
			dict1[key] = tup
			
		elif(dict2[key][4] in [0,4]):#Return "Amendment of municipal code" and "Call" to disorganized docs	
			tup = dict2[key][:3] +  (False,-1)
			dict1[key] = tup
		elif(dict2[key][4] in [8]):#not sure where to put these
			tup = dict2[key][:4] +  (50,)
			dict1[key] = tup
		elif(dict2[key][4] in [12]):#not sure where to put these
			tup = dict2[key][:4] +  (51,)
			dict1[key] = tup

	for key in keys3:
		if(dict3[key][4] in []):
			tup = dict3[key][:4] +  (0,)
			dict1[key] = tup
		elif(dict3[key][4] in [11]):
			tup = dict3[key][:4] +  (1,)
			dict1[key] = tup
		elif(dict3[key][4] in [3,14,15,16]):
			tup = dict3[key][:4] +  (2,)
			dict1[key] = tup
		elif(dict3[key][4] in [0,7,9,10,12]):
			tup = dict3[key][:4] +  (3,)
			dict1[key] = tup
		elif(dict3[key][4] in []):
			tup = dict3[key][:4] +  (4,)
			dict1[key] = tup
		elif(dict3[key][4] in []):
			tup = dict3[key][:4] +  (5,)
			dict1[key] = tup
		elif(dict3[key][4] in [2,5]):
			tup = dict3[key][:4] +  (6,)
			dict1[key] = tup
		elif(dict3[key][4] in [13]):
			tup = dict3[key][:4] +  (7,)
			dict1[key] = tup
		elif(dict3[key][4] in [1,4,6]):
			tup = dict3[key][:4] +  (8,)#City hall proceedings
			dict1[key] = tup
		elif(dict3[key][4] in [8]):
			tup = dict3[key][:4] +  (52,)#not sure
			dict1[key] = tup

	return(dict1)

