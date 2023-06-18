from flask import Flask, request
from whoosh import index
import whoosh
from whoosh.qparser import QueryParser

app = Flask(__name__)

DOCS_DIR = './docs/'
INDEX_DIR = './indexs/'


@app.route('/index',methods=['GET'])
def index():
    search_terms = request.args.get('q')
    ix = whoosh.index.open_dir(INDEX_DIR)
    ix_searcher = ix.searcher()

    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(search_terms)
    
    _result = []
    for r in ix_searcher.search(q):
        _result.append(dict(r))

    return _result

@app.route('/reindex')
def reindex():
     #####################################
    ix = index.create_in(INDEX_DIR,schema=IndexFile)
    ix = index.open_dir(INDEX_DIR)
    ix_writer = ix.writer()
    #####################################
    # get list of documents
    #####################################
    files_data = []
    file_list = os.listdir(DOCS_DIR)

    for file in file_list:
        filename = DOCS_DIR + file
        filetype = get_filetype(file)
        file_content = ""

        if filetype == 'pdf':
            file_content = extract_file_text_from_pdf(filename)

        
        file_tearms = file_content.split()
        index_doc = {
            "path":filename,
            "filename": file,
            "filetype":filetype,
            "content": file_content,
            "phone": extract_phone_number(file_tearms)
            }
        files_data.append(index_doc)
        ix_writer.add_document(path=index_doc['path'],
                               filename=index_doc['filename'],
                               filetype=index_doc['filetype'],
                               content=index_doc['content'],
                               phone=index_doc['phone'])
    ix_writer.commit()
