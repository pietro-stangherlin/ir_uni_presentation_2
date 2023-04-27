#--- importazione di moduli interi
import string
import sys
import getopt
import os.path
import json


# --- Costanti
INDEXNAME = "toyindex"
FILENAME = "esempio.json"

#--- importazione di parti di modulo ---#
from elasticsearch import Elasticsearch

#--- connettiti al server
es_server = Elasticsearch('http://localhost:9200')


# --- più impostazioni di stemming ---#

# --- aggiungi instanza "term_vector" all'indice --- #
# entualmente da ampliare
# poiché lavorarno solo sul campo "title"


with open("mapping.json", "r") as f:
    mapping = json.load(f)


# Create the index with the custom mapping
es_server.indices.create(index=INDEXNAME, body=mapping)

# data 
with open(FILENAME, "r") as f:
    data = json.load(f)

# Index the documents
for doc in data:
    res = es_server.index(index=INDEXNAME, id=doc['docid'], body=doc)
    print(res['result'])

    
