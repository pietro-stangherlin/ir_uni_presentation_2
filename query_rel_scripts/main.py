from elasticsearch import Elasticsearch
import query_functions as qf

from query import QUERIES

# constants
INDEXNAME = "toyindex"

# Elasticsearch Server 
el_server = Elasticsearch('http://localhost:9200')


# choose a query id and get the results
while True:
    user_input = input("Select a query id (int) from 1 to 5, (press enter to exit)  ")

    # exit
    if user_input == "":
        print("...closing program...")
        break
    
    # check format
    try: 
        query_id = int(user_input)

        # make query
        if query_id in QUERIES:
            response = qf.ExpandSearchFromQueryId(query_id,
                                       QUERIES,
                                       el_server,
                                       INDEXNAME)
            qf.PrettyPrintExpandQueryDict(response)
        else:
            print("The int should lie between 1 and 5")
                

    except ValueError:
        print("You should type a int, ex. 3")
    


    
    
    




