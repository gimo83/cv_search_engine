import os
import sys
import pprint
from  whoosh import index
from whoosh.qparser import QueryParser
from whoosh.fields import SchemaClass, ID, TEXT, STORED, KEYWORD


DOCS_DIR = './docs/'
INDEX_DIR = './indexs/'


class IndexFile(SchemaClass):
    path = ID(stored=True)
    filename = TEXT(stored=True)
    content = TEXT
    tags = KEYWORD
    phone = TEXT(stored=True)


search_tearms = sys.argv[1]
# print(search_tearms)

ix = index.open_dir(INDEX_DIR)
ix_searcher = ix.searcher()

qp = QueryParser("content", schema=ix.schema)
q = qp.parse(search_tearms)

for  r in ix_searcher.search(q):
    print(r)