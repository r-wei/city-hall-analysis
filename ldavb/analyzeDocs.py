import cPickle, string, numpy, getopt, sys, random, time, re, pprint

import os, json
import onlineldavb
import wikirandom

#Get a list of all the files
location = "../allDocs"
listFiles = os.listdir(location)
listFiles.remove(".DS_Store")
print(listFiles)

def documentGrab(n):
    textList = []
    count = 0;

    for doc in listFiles:
        if((count < n)):
            print(doc)
            #Open and read the document
            docText = open(location+'/'+doc, "r").read()
            docObject = json.loads(docText)
            textList.append(docObject["full_text"])
            count = count + 1
        else:
            break;

    return(textList)


print(documentGrab(5))
def main():
    """
    Downloads and analyzes a bunch of random Wikipedia articles using
    online VB for LDA.
    """

    # The number of documents to analyze each iteration
    batchsize = 1000
    # The total number of documents in Wikipedia
    D = 3.3e6
    # The number of topics
    K = 5

    # How many documents to look at
    documentstoanalyze = batchsize

    # Our vocabulary
    vocab = file('./dictnostops.txt').readlines()
    W = len(vocab)

    # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
    olda = onlineldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024., 0.7)
    # Run until we've seen D documents. (Feel free to interrupt *much*
    # sooner than this.)
    for iteration in range(0, documentstoanalyze):
        # Grab some documents
        docset = documentGrab(batchsize)

        # Give them to online LDA
        (gamma, bound) = olda.update_lambda_docs(docset)
        # Compute an estimate of held-out perplexity
        (wordids, wordcts) = onlineldavb.parse_doc_list(docset, olda._vocab)
        perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
        print '%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
            (iteration, olda._rhot, numpy.exp(-perwordbound))

        # Save lambda, the parameters to the variational distributions
        # over topics, and gamma, the parameters to the variational
        # distributions over topic weights for the articles analyzed in
        # the last iteration.
        if (iteration % 10 == 0):
            numpy.savetxt('lambda-%d.dat' % iteration, olda._lambda)
            numpy.savetxt('gamma-%d.dat' % iteration, gamma)

if __name__ == '__main__':
    main()
