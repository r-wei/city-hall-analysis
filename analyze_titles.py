import re, collections, pprint

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

def group_titles(documentDict):
#groups documents by title
#returns [k most common title groups, remaining unsorted documents]

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
            documentDict[key] = (title, text, trunc_title, True)
        else:
            documentDict[key] = (title, text, trunc_title, False)

    pp.pprint('No. of docs organized by title analysis: ' + str(total))
    pp.pprint(top_k)
    return documentDict
