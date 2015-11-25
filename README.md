# city-hall-analysis

We're experimenting with methods to organize documents at the Chicago City Clerk's Office (https://chicago.legistar.com/). 

The Clerk's Office gives each document a matter type classification (e.g., ordinance, communication, etc.) as well as a title, which serves as a short human-readable description of the document. We have attempted to organize the documents first by matter type, then by title analysis (see ad_hoc_title_analysis folder). 

We are also trying to implement some machine learning techniques to cluster subsets of these documents. Initial, more hands-on, attempts are given in grouping_via_corr_matrix. After getting a feel for the data, we hope to use latent dirichlet allocation and/or scikit.learn to implement better clustering algorithms.

We have also experimented with finding spelling errors and creating masks for the documents.
