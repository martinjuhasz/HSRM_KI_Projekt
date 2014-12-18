from datetime import datetime
import site
site.addsitedir("/usr/local/lib/python2.7/site-packages")

import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, Term, DirectoryReader
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.analysis.de import GermanAnalyzer

class LuceneSearcher(object):
    def __init__(self):
        lucene.initVM()

        # language processor and storage
        self.analyzer = GermanAnalyzer(Version.LUCENE_CURRENT)
        self.store = SimpleFSDirectory(File('./../Lucene/data/'))

    def perform_search(self, searchterm):
        # processing a query
        parser = QueryParser(Version.LUCENE_CURRENT, "content", self.analyzer)
        parser.setDefaultOperator(QueryParser.Operator.AND)

        query = parser.parse(searchterm)

        # conducting search
        searcher = IndexSearcher(DirectoryReader.open(self.store))

        start = datetime.now()
        scoreDocs = searcher.search(query, 50).scoreDocs
        duration = datetime.now() - start

        # results to return
        results = []

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            table = dict((field.name(), field.stringValue()) for field in doc.getFields())
            results.append(table)

        return results, duration


