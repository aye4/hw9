import scrapy

from quotes.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {
        "FEED_URI": "quotes.json"
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield QuoteItem(
                tags=quote.xpath("div[@class='tags']/a/text()").extract(),
                author=quote.xpath("span/small/text()").get().strip(),
                quote=quote.xpath("span[@class='text']/text()").get().strip()
            )

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
