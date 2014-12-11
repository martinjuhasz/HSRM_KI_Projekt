from controller.ArchiveCrawler import ArchiveCrawler
from controller.ArticleCrawler import ArticleCrawler

if __name__ == '__main__':
    crawler = ArchiveCrawler()
    post_links = crawler.crawl_post_links()

    article_crawler = ArticleCrawler()
    articles = []
    for link in post_links:
        article = article_crawler.crawl(link)
        if article:
            articles.append(article)

    print len(articles)

    for a in articles:
        print a.title
        print a.content
        print a.images
        print
        print