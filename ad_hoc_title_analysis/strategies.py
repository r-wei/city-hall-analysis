def apply_strategies(row):
    for strategy in strategies:
        result = strategy(row)
        if result != None:
	    return result
    return result

#Ordinance Algorithm: For each title,
#1) find the first instance of either ' for '  or ' No. ', and truncate
#2) else, find the last instance of either ' at ' or ' as ', and truncate
#3) else, truncate after n=4 words
def ordinance_parser(row):
    first_inst_pattern = re.compile(r"(.+?)( for | No\. )(.*)")
    last_inst_pattern = re.compile(r"(.+)( at | as )(.*)")

    match = first_inst_pattern.match(row)
    if match != None:
        return match.group(1) #string

    else:
        match = last_inst_pattern.match(row)
	if match != None: 
            return match.group(1)
	return match


