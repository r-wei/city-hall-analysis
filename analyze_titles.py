import re, collections, pprint
from time import time

pp = pprint.PrettyPrinter(indent=4)

#Ordinance Algorithm: For each title,
#1) find the first instance of either ' for '  or ' No. ', and truncate
#2) else, find the last instance of either ' at ' or ' as ', and truncate
def ordinance_parser(row):
    first_inst_pattern = re.compile(r"(.+?)( for | No\. | to | at )(.*)")
    last_inst_pattern = re.compile(r"(.+)( at | as )(.*)")

    match = first_inst_pattern.match(row)
    if match != None:
        return match.group(1) #string

    else:
        match = last_inst_pattern.match(row)
        if match != None: 
            return match.group(1)
        else:
      	    row_split = row.split(' ') #each title is a list of strings of words
      	    m = min(4, len(row_split))
      	    row_trunc = ' '.join(row_split[:m])
	
      	    return row_trunc 

#groups documents by title
#Consider only the documents within the top k most common trunc_titles to be grouped
#and indicate them with (title, text, trunc_title, TRUE, integer index of group).
#Ungrouped docs are indicated: (title, text, trunc_title, FALSE, -1).
def group_titles(documentDict):

    trunc_titles = []
    remaining_docs = []
    indices = []

    keys = documentDict.keys()

    for key in keys:
        title, text = documentDict[key][0:2]
   	#truncate each title using ordinance algorithm
        trunc_title = ordinance_parser(title)
        documentDict[key] = (title, text, trunc_title)

        trunc_titles = trunc_titles + [trunc_title]

    #count trunc_titles and pick out k most common
    counter = collections.Counter(trunc_titles)
    k = 17

    top_k = counter.most_common(k)
    top_titles = []
    total = 0
    for top, count in top_k:
        top_titles = top_titles + [top]
        total = total + count

    for key in keys:
        title, text, trunc = documentDict[key]
        if trunc in top_titles:
            documentDict[key] = (title, text, trunc, True, top_titles.index(trunc))
        else:
            documentDict[key] = (title, text, trunc, False, -1)

    pp.pprint('No. of docs organized by title analysis: ' + str(total))
    #pp.pprint(top_k)
    return documentDict

#given a grouped dictionary, separate out the sorted titles and the unsorted ones
def title_analysis(startDict):

	t0 = time()
	groupedDict = group_titles(startDict) #returns a dictionary of matter_id: (title, text, truncated_title, T/F is_this_doc_grouped_via_title_analysis, integer trunc_title_index)
	groupedkeys = groupedDict.keys()

	#create a dictionary of docs not organized by title analysis
	remainingDict = dict()
	for key in groupedkeys:
		if groupedDict[key][3] == False:
			remainingDict[key] = groupedDict[key]

	remainingkeys = list(remainingDict.keys())

	print("There are " + str(len(remainingkeys)) + " documents remaining.")
	print("Title analysis done in %fs" % (time() - t0))

	return(groupedDict, remainingDict)
