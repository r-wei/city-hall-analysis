import re, collections

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

def group_titles(titles, documents):
#groups documents by title
#returns [k most common title groups, remaining unsorted documents]

    trunc_titles = []
    remaining_docs = []
    indices = []
    
    #truncate each title using ordinance algorithm
    for row in titles:
        result = ordinance_parser(row)
        trunc_titles = trunc_titles + [result]

    #count trunc_titles and pick out k most common
    counter = collections.Counter(trunc_titles)
    k = 17
    top_k = counter.most_common(k)
    top_titles = []
    for title, count in top_k:
        top_titles = top_titles + [title]

    #if a title is not in the k most common, return the document for further sorting
    for j in range(len(trunc_titles)):
        if trunc_titles[j] in top_titles:
            continue
        else:
            remaining_docs = remaining_docs + [documents[j]]
            indices = indices + [j]

    result = [top_k] + [remaining_docs] + [indices]
    return result
