import functions.query_functions as qf
import functions.evaluation_funcs as ef
import json

# tested 2023-04-28: ok!
def ManualExpandedQueryPrint(query_dict, relevaces_dict, index_name, el_server):
    '''
    For the selected query_id in query_dict print:
    - initial query terms
    - expanded query terms
    - document ids retrieved with first query
    - document uds retrieved with expanded query
    - relevant document ids for that query

    @param query_dict (dict): {...,id_query : query_query_text,...}
    @param relevances_dict (dict): {...,id_query : {rel_doc1,..,rel_doc_k},...}
    @param index_name (str)
    @param el_server (Elasticsearch)

    @return (NULL)
    '''
    while True:
        user_input = input("Select a query id (int) (press enter to exit):  ")

        # exit
        if user_input == "":
            print("...closing program...")
            break
        
        # check format
        try: 
            query_id = int(user_input)

            # make query
            if query_id in query_dict:
                response = qf.ExpandSearchFromQueryId(query_id,
                                        query_dict,
                                        el_server,
                                        index_name)
                # print retrieved
                qf.PrettyPrintExpandQueryDict(response)
                # print relevant
                print(f"****Relevant docs:  {ef.RelevantQueryDocIds(int(query_id), relevaces_dict)}****")
                print("_________________________________________________________________________________\n")

            else:
                print("The int range should lie between 1 and 7")
                    

        except ValueError:
            print("You should type a int, ex. 3")
    
# to be tested
def AutomaticExpandedQueryResultFile(query_dict,
                                     relevaces_dict,
                                     index_name,
                                     el_server,
                                     file_out = "expanded_query.json"):
    '''
    For each query_id in in query_dict write on file_out (json format):
    - initial query terms
    - expanded query terms
    - document ids retrieved with first query
    - document uds retrieved with expanded query
    - relevant document ids for that query

    @param query_dict (dict): {...,id_query : query_query_text,...}
    @param relevances_dict (dict): {...,id_query : {rel_doc1,..,rel_doc_k},...}
    @param index_name (str)
    @param el_server (Elasticsearch)
    @param file_out (str): file to which write the results

    @return (NULL)
    '''
    #fout = open(file_out, "w")

    #fout.write("{\n")

    response_list = []

    for query_id in query_dict:
        response = qf.ExpandSearchFromQueryId(query_id,
                                        query_dict,
                                        el_server,
                                        index_name)
        

        # add relevant doc field
        response["relevant_docs"] = ef.RelevantQueryDocIds(int(query_id), relevaces_dict)

        # add query_id
        response["query_id"] = query_id

        # change each value of response dict to string to get a better printing
        for key in response:
            response[key] = str(response[key])
        

        
        response_list.append(response)

        #fout.write(str(response))
        #fout.write("\n")
    with open(file_out, "w") as fout:
        json.dump(response_list, fout, indent = 1)

    #fout.write("}")
    #fout.close()