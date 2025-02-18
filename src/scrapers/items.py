# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiPageItem(scrapy.Item):
    """Defines the structure of extracted wiki pages."""

    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    categories = scrapy.Field()
    links = scrapy.Field()
