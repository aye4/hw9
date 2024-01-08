# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from .authors import AuthorsSpider
from .quotes import QuotesSpider


__all__ = (
    "AuthorsSpider",
    "QuotesSpider",
)
