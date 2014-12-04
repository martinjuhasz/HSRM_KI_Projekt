from controller.ArchiveCrawler import ArchiveCrawler


if __name__ == '__main__':
    crawler = ArchiveCrawler()
    post_links = crawler.crawl_post_links()
    print post_links