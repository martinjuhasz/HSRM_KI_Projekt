from controller.ArchiveCrawler import ArchiveCrawler
from controller.ArticleCrawler import ArticleCrawler


def app():
    archive_crawler = ArchiveCrawler()
    article_crawler = ArticleCrawler()
    link_generator = archive_crawler.crawl_post_links()

    print
    print "Crawler started. Please wait a moment..."
    print

    articles = []
    for num in range(5):
        link = link_generator.next()
        article = article_crawler.crawl(link)

        if article:
            articles.append(article)
            print article

    print
    print "Articles crawled: " + str(len(articles))


if __name__ == '__main__':
    app()
