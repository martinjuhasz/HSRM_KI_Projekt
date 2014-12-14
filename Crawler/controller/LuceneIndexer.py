import site
site.addsitedir("/usr/local/lib/python2.7/site-packages")
from ArticleCrawler import ArticleCrawler

import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version



class LuceneIndexer(object):
    def __init__(self):
        lucene.initVM()

        # language processor and storage
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        store = SimpleFSDirectory(File('./data/'))

        # writes data to the index
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer, overwrite=True)
        self.writer = IndexWriter(store, config)
        #self.writer = IndexWriter(store, analyzer, overwrite=True)

    def add_article(self, article):
        # constructing a document
        doc = Document()
        doc.add(Field('url', 'http://www.hs-rm.de', Field.Store.NO, Field.Index.NOT_ANALYZED))
        doc.add(Field('body', article.content, Field.Store.YES, Field.Index.ANALYZED))
        self.writer.addDocument(doc)

    def write_to_file(self):
        # making changes permanent
        self.writer.commit()
        self.writer.close()


if __name__ == "__main__":
    test_article_big_teaser_image = "http://www.spiegel.de/wissenschaft/natur/erdoel-laeuft-in-naturschutzgebiet-in-israel-leck-in-pipeline-a-1006569.html"
    test_article_small_teaser_image = "http://www.spiegel.de/politik/ausland/anschlag-in-afghanistan-attackierte-cia-basis-plante-drohnen-angriffe-a-669739.html"
    test_image_in_article = "http://www.spiegel.de/kultur/kino/box-office-harry-potter-und-der-historische-hollywood-rekord-a-174947.html"
    test_fotostrecke = "http://www.spiegel.de/panorama/fotostrecke-silvester-feiern-und-feuerwerke-weltweit-a-174924.html"
    test_article_2001 = "http://www.spiegel.de/panorama/world-trade-center-der-anschlag-von-1993-a-156568.html"
    test_ryder_cup_results = "http://www.spiegel.de/sport/sonst/ryder-cup-das-team-der-usa-a-318353.html"


    article_crawler = ArticleCrawler()

    toAdd = article_crawler.crawl(test_article_big_teaser_image)

    lucene_indexer = LuceneIndexer()

    lucene_indexer.add_article(toAdd)
    lucene_indexer.write_to_file()


