
###################### Basic functions ########################
# tested 2023-04-27: ok!
def RelevantQueryDocIds(query_id,
                        relevances_dictionary):
    '''
    @param query_id (non-mutable): id of a query
    @param relevances_dictionary (dict): dictionaray with:
    {query_id : {relevant document ids}}

    @return (set) of relevant documentss
    '''
    return(relevances_dictionary[query_id])

######################### Evaluation measures functions ###########################
# to be tested
def IntersectionRetrievedRelevant(retrieved, relevant):
    pass

# to be tested
def ComputePrecision(retrieved_relevant, retrieved):
    pass

# to be tested
def ComputeRecall(retrieved_relevant, relevant):
    pass 


