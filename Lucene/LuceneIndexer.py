from datetime import datetime
import site
site.addsitedir("/usr/local/lib/python2.7/site-packages")
from ArticleCrawler import ArticleCrawler

import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, Term, DirectoryReader
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher


class LuceneIndexer(object):
    def __init__(self):
        lucene.initVM()

        # language processor and storage
        self.analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        self.store = SimpleFSDirectory(File('./../Lucene/data/'))

        # writes data to the index
        config = IndexWriterConfig(Version.LUCENE_CURRENT, self.analyzer, overwrite=True)
        self.writer = IndexWriter(self.store, config)
        #self.writer = IndexWriter(store, analyzer, overwrite=True)

    def add_article(self, article):
        # constructing a document
        doc = Document()
        doc.add(Field('title', article.title, Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field('description', article.description, Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field('keywords', article.keywords, Field.Store.YES, Field.Index.NOT_ANALYZED))
        doc.add(Field('date', article.date, Field.Store.YES, Field.Index.NOT_ANALYZED))
        doc.add(Field('last_modified', article.last_modified, Field.Store.YES, Field.Index.NOT_ANALYZED))
        doc.add(Field('content', article.content, Field.Store.YES, Field.Index.ANALYZED))
        if article.images:
            doc.add(Field('image_url', article.images[0][0], Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field('image_text', article.images[0][1], Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field('url', article.url, Field.Store.YES, Field.Index.NOT_ANALYZED))

        # creates document or updates if already exists
        self.writer.updateDocument(Term("url", article.url), doc)

    def write_to_file(self):
        # making changes permanent
        self.writer.commit()
        self.writer.close()



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

        print scoreDocs
        print duration

