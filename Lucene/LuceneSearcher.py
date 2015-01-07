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
from org.apache.lucene.search import IndexSearcher, BooleanQuery, TermQuery, BooleanClause
from org.apache.lucene.analysis.de import GermanAnalyzer

from org.apache.lucene.queryparser.classic import MultiFieldQueryParser

class LuceneSearcher(object):
    def __init__(self):
        lucene.initVM()

        # language processor and storage
        self.analyzer = GermanAnalyzer(Version.LUCENE_CURRENT)
        self.store = SimpleFSDirectory(File('./../Lucene/data/'))

    def perform_search(self, searchterm):
        # if there is a field in the searchterm
        """if ":" in searchterm:
            # processing a query
            parser = QueryParser(Version.LUCENE_CURRENT, "content", self.analyzer)
            parser.setDefaultOperator(QueryParser.Operator.AND)

            query = parser.parse(searchterm)

        else:
            query = BooleanQuery()
            query_title = TermQuery(Term("title", searchterm))
            query_description = TermQuery(Term("description", searchterm))
            query_content = TermQuery(Term("content", searchterm))

            #  BooleanClause.Occur.MUST for AND queries
            query.add(query_title, BooleanClause.Occur.SHOULD)
            query.add(query_description, BooleanClause.Occur.SHOULD)
            query.add(query_content, BooleanClause.Occur.SHOULD)"""

        # create QueryParser for each field to be searched
        parser_title = QueryParser(Version.LUCENE_CURRENT, "title", self.analyzer)
        parser_description = QueryParser(Version.LUCENE_CURRENT, "description", self.analyzer)
        parser_content = QueryParser(Version.LUCENE_CURRENT, "content", self.analyzer)

        # put fields together
        query = BooleanQuery()
        query.add(parser_title.parse(searchterm), BooleanClause.Occur.SHOULD)
        query.add(parser_description.parse(searchterm), BooleanClause.Occur.SHOULD)
        query.add(parser_content.parse(searchterm), BooleanClause.Occur.SHOULD)

        # conducting search
        searcher = IndexSearcher(DirectoryReader.open(self.store))

        start = datetime.now()
        hits = searcher.search(query, 5)
        score_docs = hits.scoreDocs
        count_results = hits.totalHits
        duration = datetime.now() - start

        # results to return
        results = []

        for scoreDoc in score_docs:
            doc = searcher.doc(scoreDoc.doc)
            table = dict((field.name(), field.stringValue()) for field in doc.getFields())
            results.append(table)

        return results, duration, count_results