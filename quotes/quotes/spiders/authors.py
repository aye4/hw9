import scrapy

from quotes.items import AuthorItem


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {
        "FEED_URI": "authors.json"
    }
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield scrapy.Request(
                self.start_urls[0] + quote.xpath("span/a/@href").get(),
                callback=self.get_author
            )

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def get_author(self, response):
        body = response.xpath('/html//div[@class="author-details"]')

        yield AuthorItem(
            fullname=body.xpath('h3[@class="author-title"]/text()').get().strip(),
            born_date=body.xpath('p/span[@class="author-born-date"]/text()').get().strip(),
            born_location=body.xpath('p/span[@class="author-born-location"]/text()').get().strip(),
            description=body.xpath('div[@class="author-description"]/text()').get().strip(),
        )
