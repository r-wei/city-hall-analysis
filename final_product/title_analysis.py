from strategies import *


def classifyTitle(title):
    #return the classification of a title

    #clean title
    title = title.lower()
    
    #apply classifying strategies to title
    strategies = [isTraf, isPark, isClaim, isExemp, isPubUse, isProc, isPermit, isDev, isOther, isRecog, isTax]
    result = apply_strategies(title, strategies)
    return result
