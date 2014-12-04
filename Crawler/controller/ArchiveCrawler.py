import urllib2

from BeautifulSoup import BeautifulSoup


class ArchiveCrawler(object):

    BASE_URL = "http://www.spiegel.de"
    YEAR_URL = "http://www.spiegel.de/nachrichtenarchiv/artikel-01.01.%s.html"
    DEFAULT_YEARS_TO_CRAWL = ["2014", "2013"]
    DEBUG = True


    def crawl_post_links(self, years=DEFAULT_YEARS_TO_CRAWL):

        # crawl for all daily pages for years
        return_links = []
        day_links = self.crawl_years(years)

        # for each day link crawl for all posts
        for day_link in day_links:
            links = self.crawl_day_link(day_link)
            if links is not None:
                return_links += links

                if ArchiveCrawler.DEBUG:
                    return return_links

        return return_links

    def crawl_day_link(self, day_link):

        # extract content to bs
        response = urllib2.urlopen(day_link)
        html = response.read()
        soup = BeautifulSoup(html)

        # search for main column and return all links
        main_column = soup.find('div', {'class': 'column-wide'})
        links = main_column.findAll('a')
        return_links = [ArchiveCrawler.BASE_URL + link['href'] for link in links]

        return return_links


    def crawl_years(self, years_to_crawl):

        return_links = []

        for year in years_to_crawl:

            # extract content to bs
            response = urllib2.urlopen(ArchiveCrawler.YEAR_URL % year)
            html = response.read()
            soup = BeautifulSoup(html)

            # find right column and loop through each module section
            right_column = soup.find('div', {'class': 'column-small'})
            modules = right_column.findAll('div', {'class': 'module-box'})
            for module in modules:

                # only search for links when year is in module title
                title = module.find('div', {'class': 'module-title'})
                if title is not None and year in title.text:
                    days = module.find('table', {'class': 'news-archive-table'})
                    if days is not None:
                        links = days.findAll('a')
                        if links is not None:
                            return_links += [ArchiveCrawler.BASE_URL + link['href'] for link in links]

                            if ArchiveCrawler.DEBUG:
                                return return_links

        return return_links
