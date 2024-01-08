import json
from itemadapter import ItemAdapter
import scrapy
from scrapy.crawler import CrawlerProcess


class AuthorItem(scrapy.Item):
    fullname = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()


class QuoteItem(scrapy.Item):
    author = scrapy.Field()
    quote = scrapy.Field()
    tags = scrapy.Field()


class QuotesPipeline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if isinstance(item, AuthorItem):
            self.authors.append(adapter.asdict())
        if isinstance(item, QuoteItem):
            self.quotes.append(adapter.asdict())

    def close_spider(self, spider):
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=2)
        with open("authors.json", "w", encoding="utf-8") as f:
            json.dump(self.authors, f, ensure_ascii=False, indent=2)


class QuotesSpider(scrapy.Spider):
    name = 'quotes_with_authors'
    custom_settings = {"ITEM_PIPELINES": {QuotesPipeline: 300}}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield QuoteItem(
                tags=quote.xpath("div[@class='tags']/a/text()").extract(),
                author=quote.xpath("span/small/text()").get().strip(),
                quote=quote.xpath("span[@class='text']/text()").get().strip()
            )

            yield scrapy.Request(
                self.start_urls[0] + quote.xpath("span/a/@href").get(),
                callback=self.parse_author
            )

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        author = response.xpath('/html//div[@class="author-details"]')

        def x(string) -> str:
            return author.xpath(string).get().strip()

        yield AuthorItem(
            fullname=x('h3[@class="author-title"]/text()'),
            born_date=x('p/span[@class="author-born-date"]/text()'),
            born_location=x('p/span[@class="author-born-location"]/text()'),
            description=x('div[@class="author-description"]/text()')
        )


def main():
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()


if __name__ == '__main__':
    main()
