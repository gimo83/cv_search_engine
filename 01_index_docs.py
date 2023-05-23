from PyPDF2 import PdfReader
import os
import pprint
from  whoosh import index
from whoosh.fields import SchemaClass, ID, TEXT, STORED, KEYWORD


DOCS_DIR = './docs/'
INDEX_DIR = './indexs/'

class IndexFile(SchemaClass):
    path = ID(stored=True)
    filename = TEXT(stored=True)
    filetype = TEXT(stored=True)
    content = TEXT(stored=True)
    tags = KEYWORD
    phone = TEXT(stored=True)





def extract_file_text_from_pdf(filename):
    _text = ""
    reader = PdfReader(filename)

    for page in reader.pages:
        _text += page.extract_text()
    
    return _text

def extract_file_text_from_doc(filename):
    _text = ""

    return _text

def extract_phone_number(file_tearms):
    _phone_number = ''
    for tearm in file_tearms:
        if len(tearm) > 4 and ( tearm.find('966') >= 0 or tearm.find('05') >= 0 ) :
            _phone_number = tearm
    
    return _phone_number

def get_filetype(filename):
    _filetype = ''
    _i = filename.rfind('.')
    _filetype = filename[_i+1:]

    return _filetype





def main():
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
    
    # pprint.pprint(files_data)

if __name__ == "__main__":
    main()
