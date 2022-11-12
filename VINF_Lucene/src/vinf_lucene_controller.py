import lucene
import json

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
    def __init__(self, index_directory):
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        self.data_directory = lucene_folder + '/data/'

        self.index_directory = index_directory
        self.index_dir = index_directory
        self.dir_wrapper = NIOFSDirectory(Paths.get(self.index_dir))
        self.analyzer = StandardAnalyzer()
        #self.analyzer = LimitTokenCountAnalyzer(self.analyzer, 5000)
        self.writer_config = IndexWriterConfig(self.analyzer)
        self.writer = IndexWriter(self.dir_wrapper, self.writer_config)

        self.reader = None
        self.searcher = None

    def create_index(self, infilename):
        
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
            doc.add(Field("death_date", record['death_date'], TextField.TYPE_STORED))
            doc.add(Field("birth_place", record['birth_place'], TextField.TYPE_STORED))
            doc.add(Field("death_place", record['death_place'], TextField.TYPE_STORED))
            self.writer.addDocument(doc)
        self.writer.commit()
        print("created idx")
        pass
    
    def search_index(self, options, tokens, operator):
        if self.reader is None:
            self.reader = DirectoryReader.open(self.dir_wrapper)
            self.searcher = IndexSearcher(self.reader)
        else:
            new_reader = DirectoryReader.openIfChanged(self.reader)
            if new_reader:
                self.reader = new_reader
                self.searcher = IndexSearcher(self.reader)
        parser = QueryParser("title", self.analyzer)
        if operator.lower() in ['and', '+']:
            parser.setDefaultOperator(QueryParser.Operator.AND)
        else:
            parser.setDefaultOperator(QueryParser.Operator.OR)
        query = parser.parse(tokens)
        scoreDocs = self.searcher.search(query, 10).scoreDocs
        return scoreDocs
        pass


luc_controller = VINF_Lucene_Controller(lucene_folder + "/data")
#luc_controller.create_index(root_folder + "/VINF_Parser/data/records.json")
docs = luc_controller.search_index(None,"Abraham", "OR")
print(docs)
