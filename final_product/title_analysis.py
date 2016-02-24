class TitleTermClassifier(object):
    """Instantiate a TitleTermClassifier with a list of title terms and a classification label"""

    def __init__(self,label,terms):
        """"parkingClassifier = TitleTermClassifier("Parking",["permit parking", "parking permit"])"""
        self.label = label
        self.terms = terms

    def test_terms(self, title):
        if (any(term in title for term in self.terms)):
            return self.label
        return None

    def __call__(self, title):
        return self.test_terms(title)

class ShortCircuitClassifier(TitleTermClassifier):
    def __call__(self, title):
        if (title.startswith("payment ")):
            return "Claims"
        elif ("special city council meeting" in title):
            return None
        else:
            return self.test_terms(title)



def apply_strategies(title, strategies):
    #apply classification strategies one-by-one to the title
 
    for strat in strategies:
        result = strat(title)
        if result != None:
            return result

    return result


def classifyTitle(title):
    #return the classification of a title

    #clean title
    title = title.lower()
    
    #apply classifying strategies to title
    strategies = [TitleTermClassifier("Traffic", ["tow zone", "tow-away zone", "buffer zone", "traffic sign", 
                                                  "traffic regulation", "vehicle weight", "parking prohibited", 
                                                  "traffic direction"]), 
		  TitleTermClassifier("Parking", ['permit parking', 'parking permit']),
                  ShortCircuitClassifier("Claims", ["refund(s)", "claim"]), 
		  TitleTermClassifier("Exemptions", ["free permit(s)", "cancellation", "exemption", "waiver",
                                                     "refund of fee"]), 
		  TitleTermClassifier("Public_Use", ["privilege in public way", "privilege in the public way", 
		                                     "canopy(s)", "awning(s)", "sidewalk cafe(s)", 
		                                     "issuance of permits", "vacation of public alley"]), 
                  ShortCircuitClassifier("Proceedings", ["city council journal", "city council meeting", 
		                                     "oath of office", "appointment of"]),
		  TitleTermClassifier("Permit", ['tag day permit(s)', 'issuance of special event license', 
                                                 'issuance of special event permit']), 
		  TitleTermClassifier("Development", ['of city-owned property', 'zoning reclassification map']), 
		  TitleTermClassifier("Other", ["scope of services, budget and management agreement"]), 
		  TitleTermClassifier("Recognition", ["honorary street", "tribute", "extended to", "congratulations"]), 
		  TitleTermClassifier("Tax", ["(tif)", "tax incentive", "tax increment financing"])
		  ]
    result = apply_strategies(title, strategies)
    return result

