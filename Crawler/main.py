from controller.ArchiveCrawler import ArchiveCrawler
from controller.ArticleCrawler import ArticleCrawler
from Lucene.LuceneIndexer import LuceneIndexer


def app():
    archive_crawler = ArchiveCrawler()
    article_crawler = ArticleCrawler()
    link_generator = archive_crawler.crawl_post_links()
    lucene_indexer = LuceneIndexer()

    print
    print "Crawler started. Please wait a moment..."
    print

    for num in range(5):
        try:
            link = link_generator.next()
            article = article_crawler.crawl(link)

            if article:
                # add article to lucene index
                lucene_indexer.add_article(article)
                print article
        except Exception, e:
            print "Log: could not crawl article " + str(article)

    print
    print "Crawler ended. Saving..."
    print

    # commit and write index
    lucene_indexer.write_to_file()


if __name__ == '__main__':
    app()
