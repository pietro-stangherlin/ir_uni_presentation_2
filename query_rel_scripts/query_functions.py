from elasticsearch import Elasticsearch
import json

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
  "query": {
    "match": {
      "title": query_text
    }
  },
  "_source": ["_id"],
  "size": doc_num
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

# to be tested
def ChooseFirst(doc_ids_list):
    '''
    @param doc_ids_list (list): list of sorted by ranking doc ids

    @ return a list iwth the first id (first element of the list)
    '''
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

# to be tested
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

    @return (list): list of 2 list:
    first list: list of document ids retrieved in the first search
    second list: list of document ids retrieved in the second search after expansion

    '''
    query_first_dict = MakeSearchDict(query_text, doc_num)

    # first retrieval doc ids list
    doc_ids_list_first = ElSearchDocIds(query_first_dict,
                                             el_server,
                                             indexname)
    
    # get doc ids based on criterion function among doc retrieved
    criterion_doc_ids =  criterion_func(doc_ids_list_first)

    # for each selected doc get its term vector (descriptors/tokens)
    # and make a list with all term vectors

    tokens_list = []

    for doc_id in criterion_doc_ids:
        tokens_list.extend(GetDocTokensById(doc_id,
                                            indexname,
                                            el_server))
    # debug
    print(f" tokens_list = {tokens_list}")
        
    # concatenate the tokens in one string and also with the starting query string
    new_query_text = ConcatenateString(query_text,
                                       FromListToString(tokens_list))
    # debug
    print(f" new_query_text = {new_query_text}")
    
    # make new query dict
    new_query_dict = MakeSearchDict(new_query_text, doc_num)

    # new retrieval doc ids list
    doc_ids_list_new = ElSearchDocIds(new_query_dict,
                                             el_server,
                                             indexname)
    
    return([doc_ids_list_first, doc_ids_list_new])
    
     
# testing
if __name__ == "__main__":
    def main():

        el_server = Elasticsearch('http://localhost:9200')
        QUERYTEXT = "dolphin"
        INDEXNAME = "toyindex"

        #--- test MakeSearchDict() ---#
      
        #query_dict = MakeSearchDict(QUERYTEXT, 4)

        #response = el_server.search(index=INDEXNAME,body=query_dict)
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
        print(ExpandSearchFromSearch(QUERYTEXT,
                                     el_server,
                                     INDEXNAME))




    main()