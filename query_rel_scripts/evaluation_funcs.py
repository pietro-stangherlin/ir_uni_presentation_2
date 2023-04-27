# to be tested
def RelevantQueryDocIds(query_id,
                        relevances_dictionary):
    '''
    @param query_id (non-mutable): id of a query
    @param relevances_dictionary (dict): dictionaray with:
    {query_id : {relevant document ids}}

    @return (set) of relevant documentss
    '''
    return(relevances_dictionary[query_id])


def IntersectionRetrievedRelevant(retrieved, relevant):
    pass


def ComputePrecision(retrieved_relevant, retrieved):
    pass


def ComputeRecall(retrieved_relevant, relevant):
    pass 

