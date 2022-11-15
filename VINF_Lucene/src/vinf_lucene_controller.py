import lucene
import json
import datetime

from java.nio.file import Paths                                                                         # type: ignore
from org.apache.lucene.store import NIOFSDirectory                                                      # type: ignore
from org.apache.lucene.analysis.standard import StandardAnalyzer                                        # type: ignore
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer                            # type: ignore
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader       # type: ignore
from org.apache.lucene.search import IndexSearcher                                                      # type: ignore
from org.apache.lucene.queryparser.classic import QueryParser                                           # type: ignore
from org.apache.lucene.document import Document, Field, StringField, TextField, StoredField, FieldType  # type: ignore

import os
import sys
#define the root folder so that python recognises packages
lucene_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_folder = os.path.abspath(os.path.dirname(os.path.abspath(lucene_folder)))
sys.path.append(root_folder)

from vinf_date import *
from vinf_utils import *

class VINF_Lucene_Controller:
    def __init__(self):
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        self.data_dir = lucene_folder + '/data'
        self.index_dir = self.data_dir + '/index'
        self.dir_wrapper = NIOFSDirectory(Paths.get(self.index_dir))
        self.analyzer = StandardAnalyzer()
        #self.analyzer = LimitTokenCountAnalyzer(self.analyzer, 5000)
        self.writer_config = IndexWriterConfig(self.analyzer)
        self.writer = IndexWriter(self.dir_wrapper, self.writer_config)
        self.reader = None
        self.searcher = None

    
    def get_record_from_doc(self, hit):
        doc = self.searcher.doc(hit.doc)
        title = doc.get("title")
        categories = doc.get("categories")
        birth_date = doc.get("birth_date")
        birth_date_is_bc = doc.get("birth_date_is_bc")
        death_date = doc.get("death_date")
        death_date_is_bc = doc.get("death_date_is_bc")
        birth_place = doc.get("birth_place")
        death_place = doc.get("death_place")
        record = {
            'title' : title,
            'categories' : categories,
            'birth_date' : datetime.datetime.strptime(birth_date, "%Y-%m-%d %H:%M:%S").date() if birth_date != "None" else None,
            'birth_date_is_bc' : True if birth_date_is_bc == "true" else False,
            'death_date' : datetime.datetime.strptime(death_date, "%Y-%m-%d %H:%M:%S").date() if death_date != "None" else None,
            'death_date_is_bc' : True if death_date_is_bc == "true" else False,
            'birth_place' : birth_place,
            'death_place' : death_place,
        }
        return record

    def create_index(self, infilename):
        logging.info("creating index ...")
        logging.info("opening input file: " + infilename)
        records = {}
        if ".json" in infilename:
            f = open(infilename)
            records = json.load(f)
        
        for record in records.values():
            doc = Document()
            doc.add(Field("title", record['title'], TextField.TYPE_STORED))
            doc.add(Field("name", record['name'], TextField.TYPE_STORED))
            doc.add(Field("categories", record['categories'], TextField.TYPE_STORED))
            doc.add(Field("birth_date", record['birth_date'], TextField.TYPE_STORED))
            doc.add(Field("birth_date_is_bc", record['birth_date_is_bc'], TextField.TYPE_STORED))
            doc.add(Field("death_date", record['death_date'], TextField.TYPE_STORED))
            doc.add(Field("death_date_is_bc", record['death_date_is_bc'], TextField.TYPE_STORED))
            doc.add(Field("birth_place", record['birth_place'], TextField.TYPE_STORED))
            doc.add(Field("death_place", record['death_place'], TextField.TYPE_STORED))
            self.writer.addDocument(doc)
        self.writer.commit()
        logging.info("index created in location: "+ self.index_dir)
        pass
    
    def search_index(self, attribute, tokens, operator):
        if self.reader is None:
            self.reader = DirectoryReader.open(self.dir_wrapper)
            self.searcher = IndexSearcher(self.reader)
        else:
            new_reader = DirectoryReader.openIfChanged(self.reader)
            if new_reader:
                self.reader = new_reader
                self.searcher = IndexSearcher(self.reader)
        parser = QueryParser(attribute, self.analyzer)
        if operator == "AND":
            parser.setDefaultOperator(QueryParser.Operator.AND)
        else:
            parser.setDefaultOperator(QueryParser.Operator.OR)
        query = parser.parse(tokens)
        scoreDocs = self.searcher.search(query, 10).scoreDocs
        return scoreDocs
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    luc = VINF_Lucene_Controller()
    luc.create_index(root_folder + '/VINF_Parser/data/records.json')

