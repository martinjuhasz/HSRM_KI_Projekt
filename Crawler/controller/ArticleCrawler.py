# -*- coding: utf-8 -*-
import urllib2
import re
from BeautifulSoup import BeautifulSoup
from model.Article import Article
from other.config import Config
import time


class ArticleCrawler(object):
    """
    Extracts data (e.g. date, title, content) of an article of Spiegel Online.
    """
    def crawl(self, article_url):
        """
        Extracts data (e.g. date, title, content) of an article of Spiegel Online.

        :param article_url: url of article to crawl
        :return: Article object filled with info of the article.
        :return: None if no real article
        """
        # extract content to bs
        response = urllib2.urlopen(article_url)
        time.sleep(Config.REQUEST_SLEEP_TIME)
        html = response.read()
        soup = BeautifulSoup(html)

        # return None if site is no article
        type = soup.find("meta", {"property": "og:type"})
        if not type or type["content"] != "article":
            print 'Log: ignored ' + article_url
            return None


        new_article = Article()

        # extract date & last_modified date
        new_article.date = soup.find("meta", {"name": "date"})["content"].encode('utf-8').strip()
        new_article.last_modified = soup.find("meta", {"name": "last-modified"})["content"].encode('utf-8').strip()

        # extract title, remove "- SPIEGEL ONLINE"
        new_article.title = soup.find("meta", {"property": "og:title"})["content"].replace("- SPIEGEL ONLINE", "").encode('utf-8').strip()
        # extract description
        new_article.description = soup.find("meta", {"property": "og:description"})["content"].encode('utf-8').strip()
        # extract keywords
        new_article.keywords = soup.find("meta", {"name": "keywords"})["content"].encode('utf-8').strip()

        # get content html
        article_html = soup.find('div', {'class': 'article-section clearfix'})

        # extract images in text
        for image_intext in article_html.findAll('div', attrs={"class": re.compile(r".*\bjs-module-box-image\b.*")}):
            image_intext.extract()
            # TODO: crawl image gallery and get images for article

        # kill all script and style elements
        for script in article_html(["script", "style"]):
            script.extract()

        new_article.content = article_html.getText().encode('utf-8').strip()

        # get teaser image
        teaser_img_html = soup.find("div", attrs={"id": "js-article-top-wide-asset"})
        if teaser_img_html:
            teaser_img = teaser_img_html.find("img")
            if teaser_img:
                new_article.images.append((teaser_img["src"].encode('utf-8').strip(), teaser_img["title"].encode('utf-8').strip()))

        return new_article


if __name__ == "__main__":
    test_article_big_teaser_image = "http://www.spiegel.de/wissenschaft/natur/erdoel-laeuft-in-naturschutzgebiet-in-israel-leck-in-pipeline-a-1006569.html"
    test_article_small_teaser_image = "http://www.spiegel.de/politik/ausland/anschlag-in-afghanistan-attackierte-cia-basis-plante-drohnen-angriffe-a-669739.html"
    test_image_in_article = "http://www.spiegel.de/kultur/kino/box-office-harry-potter-und-der-historische-hollywood-rekord-a-174947.html"
    test_fotostrecke = "http://www.spiegel.de/panorama/fotostrecke-silvester-feiern-und-feuerwerke-weltweit-a-174924.html"
    test_article_2001 = "http://www.spiegel.de/panorama/world-trade-center-der-anschlag-von-1993-a-156568.html"
    test_ryder_cup_results = "http://www.spiegel.de/sport/sonst/ryder-cup-das-team-der-usa-a-318353.html"


    article_crawler = ArticleCrawler()

    new_article1 = article_crawler.crawl(test_article_big_teaser_image)
    print new_article1.title
    print new_article1.content
    print new_article1.images
    print
    print
    print

    new_article2 = article_crawler.crawl(test_fotostrecke)
    print new_article2.title
    print new_article2.content
    print new_article2.images