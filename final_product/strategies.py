
def isPark(title):
    #classify a title as "Parking" if it contains a term from park_terms

    park_terms = ["permit parking", "parking permit"]
    if any(term in title for term in park_terms):
        return "Parking"
    else:
        return None

def isClaim(title):
    #classify a title as "Claims" if it contains a term from claim_terms
    #or starts with "payment "

    claim_terms = ["refund(s)", "claim"]
    if any(term in title for term in claim_terms):
        return "Claims"
    elif title.startswith("payment "):
        return "Claims"
    else:
        return None

def isPubUse(title):
    #classify a title as "Public Use" if it contains a term from pub_terms

    pub_terms = ["public way", "canopy(s)", "awning(s)", "sidewalk cafe(s)", "issuance of permits"]
    if any(term in title for term in pub_terms):
        return "Public_Use"
    else:
        return None

def isRecog(title):
    #classify a title as "Recognition" if it contains a term from recog_terms

    recog_terms = ["honorary street", "tribute", "extended to"]
    if any(term in title for term in recog_terms):
        return "Recognition"
    else:
        return None

def isExemp(title):
    #classify a title as "Exemptions" if it contains a term from exemp_terms

    exemp_terms = ["free permit(s)", "cancellation", "exemption", "waiver"]
    if any(term in title for term in exemp_terms):
        return "Exemptions"
    else:
        return None

def isProc(title):
    #classify a title as "Proceedings" if it contains a term from proc_terms
    #do not classify if it contains "special city council meeting"

    proc_terms = ["city council journal", "city council meeting", "oath of office"]
    if "special city council meeting" in title:
        return None
    elif any(term in title for term in proc_terms):
        return "Proceedings"
    else:
        return None

def isTraf(title):
    #classify a title as "Traffic" if it contains a term from traf_terms

    traf_terms = ["tow zone", "tow-away zone", "buffer zone", "traffic sign", "traffic regulation", "vehicle weight", "parking prohibited", "traffic direction"]
    if any(term in title for term in traf_terms):
        return "Traffic"
    else:
        return None

def isPermit(title):
    #classify a title as "Permit" if it contains a term from permit_terms

    permit_terms = ['tag day permit(s)', 'issuance of special event license(s) and/or permit(s)']
    if any(term in title for term in permit_terms):
        return "Permit"
    else:
        return None

def isDev(title):
    #classify a title as "Development" if it contains a term from dev_terms

    dev_terms = ['sale of city-owned property', 'zoning reclassification map']
    if any(term in title for term in dev_terms):
        return "Development"
    else:
        return None

def isOther(title):
    #classify a title as "Other" if it contains a term from other_terms

    other_terms = ["scope of services, budget and management agreement"]
    if any(term in title for term in other_terms):
        return "Other"
    else:
        return None

def isTax(title):
    #classify a title as "Tax" if it contains a term from tax_terms

    tax_terms = ["(tif)", "tax incentive"]
    if any(term in title for term in tax_terms):
        return "Tax"
    else:
        return None

def apply_strategies(title, strategies):
    #apply classification strategies one-by-one to the title
 
    for strat in strategies:
        result = strat(title)
        if result != None:
            return result

    return result
