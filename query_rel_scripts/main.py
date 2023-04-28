from elasticsearch import Elasticsearch
from functions import final_query_funcs as fqf

from data.query import QUERIES
from data.relevances import RELEVANCES

# constants
INDEXNAME = "toyindex"

# Elasticsearch Server 
el_server = Elasticsearch('http://localhost:9200')


choose = input("Digit 'm' for manual search and 'a' for automatic search:   ")

if choose == "m":
    # choose a query id and get the results
    fqf.ManualExpandedQueryPrint(QUERIES,
                             RELEVANCES,
                             INDEXNAME,
                             el_server)
    
elif choose == "a":
    fqf.AutomaticExpandedQueryResultFile(QUERIES,
                             RELEVANCES,
                             INDEXNAME,
                             el_server)
    


    
    
    




