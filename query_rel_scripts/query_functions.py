# tested 2023-04-26: ok !
def MakeSearchDict(query_text, doc_num = 10):
    '''
    make Elasticsearch query dict from a string
    assuming to use only the "title" field

    @param query (str) query string
    @param doc_num (int) number of document retrieved (by descending ranking)

    @return searc_dict (dict) a query dictionary 
        that can be used to search in Elasticsearch
    '''
    search_dict = {
        "size": doc_num,
  "query": {
    "match": {
      "title": query_text
    }
  },
  "_source": ["_id"]
}
    
    return search_dict

# tested 2023-04-26: ok!
def GetAllDocIdFromSearchDictResponse(response_dict, output_list = True):
    '''
    @param response_dict (dict) dictionary of an ElasticSearch search response
    @param outputlist (bool) if TRUE returns a list instead of a dict

    @return 
    if output_list == True:
    list (list) of documents id sorted by retrieval ranking

    if output_list == False:
    id_rel_dict (dict) dictionary with each document retrieved 
    and its relevance score like {id_doc : relevance_score}
    with id_doc (int), relevance_score (float)
    '''
    response_hits_list = response_dict["hits"]["hits"]

    # -- if output_list == True ---#
    #--- return sorted list ---# 
    if output_list == True:
        id_rel_list = []
        for hit in response_hits_list:
          id_rel_list.append(hit["_id"])
        
        return id_rel_list



    #--- if output_list == False ---#
    #--- return dictionary ---#
    id_rel_dict = {}

    for hit in response_hits_list:
        id_rel_dict[hit["_id"]] = [hit["_score"]]

    return id_rel_dict

#  tested 2023-04-26: ok!
def GetDocTokensById(doc_id, index_name, el_server, field = "title"):
    '''
    @param doc_id (int) or (str): document id
    @param index_name (str): name of the index
    @param el_server (Elasticsearch): elasticsearch server running
    @param field (str): field of the source file where to look for tokens

    @return (list) list of documents descriptors (tokens) used to make the index
    '''
    pass

    term_vectors_dict = dict(el_server.termvectors(index = index_name,
                                                   id = doc_id,
                                                   fields = field))
    return(list(term_vectors_dict["term_vectors"]["title"]["terms"]))

#  tested 2023-04-26: ok!
def FromListToString(list):
    '''
    @param list (list) of strings (Str)

    @return string (str) containing the list elements joined using " " as separator
    '''
    return(" ".join(list))

# tested 2023-04-26: ok! 
def ConcatenateString(str1, str2):
    '''
    @param str1, str2 (str) strings to be concatenated

    @return str1 + str2 (str)
    '''
    return(str1 + " " + str2)

# tested 2023-04-26: ok!
def ChooseFirst(doc_ids_list):
    '''
    @param doc_ids_list (list): list of sorted by ranking doc ids

    @ return a list iwth the first id (first element of the list)
    '''
    if len(doc_ids_list) == 0:
        return []

    return([doc_ids_list[0]])

# tested 2023-04-26: ok! 
def ElSearchDocIds(query_dict, el_server, indexname):
    '''
    @param query_dict (dict): query dictionary
    @param el_server (Elasticsearch): Elasticsearch server running
    @param indexname (str): name of the index

    @return list of k(specified by the query) document ids sorted by ranking (asc)
    '''
    response = el_server.search(index=indexname,body=query_dict)
    doc_retr_list = GetAllDocIdFromSearchDictResponse(response)
    return(doc_retr_list)

# tested 2023-04-27: ok!
def ExpandSearchFromSearch(query_text,
                          el_server,
                          indexname,
                          criterion_func = ChooseFirst,
                          doc_num = 10):
    '''
    1) Make a first search based on query_text
    2) Based on some criterion function select some of the retrieved documents
    3) Define a new query text with the text from the starting query
    concatenated with the descriptors of the retrieved documents choosen
    4) retrive the documents id found in this way

    @param query_text (str): query text
    @param el_server (Elasticsearch): Elasticsearch server running
    @param indexname (str): name of the index
    @param criterion_func (function): function that select the doc ids from the first search 
    @param doc_num (int): number of retrieved documents shown in a search 

    @return (dict):
    {"intial_doc_ids_list": [...],
    "expanded_doc_ids_list": [...]",
    "initial_query_text": "...",
    "expanded_query_text"}
    first list: list of document ids retrieved in the first search
    second list: list of document ids retrieved in the second search after expansion

    '''
    query_first_dict = MakeSearchDict(query_text, doc_num)

    # first retrieval doc ids list
    initial_doc_ids_list = ElSearchDocIds(query_first_dict,
                                             el_server,
                                             indexname)
    
    # get doc ids based on criterion function among doc retrieved
    # list
    criterion_doc_ids =  criterion_func(initial_doc_ids_list)

    # for each selected doc get its term vector (descriptors/tokens)
    # and make a list with all term vectors
    
    tokens_list = []

    for doc_id in criterion_doc_ids:
        tokens_list.extend(GetDocTokensById(doc_id,
                                            indexname,
                                            el_server))
    # debug
    # print(f" tokens_list = {tokens_list}")
        
    # concatenate the tokens in one string and also with the starting query string
    expanded_query_text = ConcatenateString(query_text,
                                       FromListToString(tokens_list))
    # debug
    # print(f" new_query_text = {expanded_query_text}")
    
    # make new query dict
    expanded_query_dict = MakeSearchDict(expanded_query_text, doc_num)

    # new retrieval doc ids list
    expanded_doc_ids_list = ElSearchDocIds(expanded_query_dict,
                                             el_server,
                                             indexname)
    
    returned_dic = {"intial_doc_ids_list": initial_doc_ids_list,
    "expanded_doc_ids_list": expanded_doc_ids_list,
    "initial_query_text": query_text,
    "expanded_query_text": expanded_query_text}
    
    return(returned_dic)
    
# tested 2023-04-27: ok!
def ExpandSearchFromQueryId(key,
                        dicto,
                        el_server,
                        indexname,
                        criterion_func = ChooseFirst,
                        doc_num = 10):
    '''
    @param key (non_mutable) dictionary key: query text id
    @param dicto (dict) dictionary containig query text id as key and query text as value
    @param el_server (Elasticsearch): Elasticsearch server running
    @param indexname (str): name of the index
    @param criterion_func (function): function that select the doc ids from the first search 
    @param doc_num (int): number of retrieved documents shown in a search

    @return (dict):
    {"intial_doc_ids_list": [...],
    "expanded_doc_ids_list": [...]",
    "initial_query_text": "...",
    "expanded_query_text"}
    first list: list of document ids retrieved in the first search
    second list: list of document ids retrieved in the second search after expansion
    '''
    return(ExpandSearchFromSearch(dicto[key],
                          el_server,
                          indexname,
                          criterion_func,
                          doc_num))    

# tested 2023-04-27: ok!
def PrettyPrintExpandQueryDict(dicto):
    '''
    @param dicto (dict): dicitionary as returned in ExpandSearchFromSearch
    '''
    key_iqt = "initial_query_text"
    key_eqt = "expanded_query_text"
    key_idli = "intial_doc_ids_list"
    key_edli = "expanded_doc_ids_list"

    print("*******************************************************************************")
    print(f"{key_iqt} : {dicto[key_iqt]}")
    print(f"{key_eqt} : {dicto[key_eqt]}")
    print(f"{key_idli} : {dicto[key_idli]}")
    print(f"{key_edli} : {dicto[key_edli]}")
    print("*******************************************************************************")
    

# testing
if __name__ == "__main__":
    from elasticsearch import Elasticsearch
    def main():

        el_server = Elasticsearch('http://localhost:9200')
        QUERYTEXT = "dolphin"
        INDEXNAME = "toyindex"

        #--- test MakeSearchDict() ---#
      
        # query_dict = MakeSearchDict(QUERYTEXT, 4)

        # response = el_server.search(index=INDEXNAME,body=query_dict)
        # print(response)
 

        #--- test GetAllDocIdFromSearchDictResponse() ---#
        #response_dict = dict(response)
        ##print(response_dict)

        #id_rel_dict = GetAllDocIdFromSearchDictResponse(response_dict, True)

        #print(id_rel_dict)

        # --- test GetTokensById() ---#
        # print(GetDocTokensById("1", INDEXNAME,el_server))

        #--- test FromListToString ---#
        #print(FromListToString(["ddq", "5333" ,"e2e2e"]))

        # --- test ConcatenateString ---#
        # print(ConcatenateString("aa bbb cc", "fff kk"))

        #--- test ElSearchDocIds ---#
        # print(ElSearchDocIds(query_dict, el_server, INDEXNAME))

        # --- test ExpandSearchFromSearch ---#
        # print(ExpandSearchFromSearch(QUERYTEXT,el_server,INDEXNAME))
        
        # --- test ExpandSearchFromQueryId ---#
        # from query import QUERIES
        # print(ExpandSearchFromQueryId(2, QUERIES,el_server,INDEXNAME))




    main()