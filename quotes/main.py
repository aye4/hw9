from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from quotes.spiders import QuotesSpider, AuthorsSpider


def main():
    process = CrawlerProcess(get_project_settings())

    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)

    process.start()


if __name__ == '__main__':
    main()
