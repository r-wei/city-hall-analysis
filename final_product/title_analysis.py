from strategies import *


def classifyTitle(title):
    #return the classification of a title

    #clean title
    title = title.lower()
    
    #apply classifying strategies to title
    strategies = [isPark, isClaim, isPubUse, isProc, isExemp, isPermit, isDev, isOther, isTraf, isRecog, isTax]
    result = apply_strategies(title, strategies)
    return result
