"""Forgotten Realms Lore Scraper"""

from urllib.parse import urljoin

import scrapy

from src.scrapers.items import WikiPageItem

BASE_URL = "https://forgottenrealms.fandom.com"


class ForgottenRealmsSpider(scrapy.Spider):
    """
    A Scrapy spider for crawling the Forgotten Realms Wiki.

    This spider starts at the main Forgotten Realms wiki page and recursively follows
    internal links to extract:
    - Titles
    - Page content
    - Categories
    - Links to other wiki pages

    The extracted data is processed into a structured `WikiPageItem` and sent to the
    `WikiGraphPipeline` for further storage in a NetworkX graph and FAISS vector database.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): Domains that the spider is allowed to crawl.
        start_urls (list): The starting page(s) for the crawl.
        visited_pages (set): A set of already visited URLs to prevent duplicate crawling.
    """

    name = "forgotten_realms"
    allowed_domains = ["forgottenrealms.fandom.com"]
    start_urls = [urljoin(BASE_URL, "/wiki/Forgotten_Realms")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited_pages = set()

    def parse(self, response):
        """Extracts page content and links, yielding structured data."""
        page_url = response.url

        # Avoid duplicate processing
        if page_url in self.visited_pages:
            return  # Stop processing if we've already visited this page
        self.visited_pages.add(page_url)

        # Extract title
        title = response.css("#firstHeading > span::text").get()
        title = title.strip() if title else "Unknown"

        # Extract text content
        paragraphs = response.css("div.mw-parser-output p::text").getall()
        content = " ".join(paragraphs).strip()

        # Extract categories
        categories = response.css(".page-header__categories-in + a::text").getall()
        categories = categories if categories else ["Uncategorized"]

        # Extract links to other wiki pages
        links = [
            urljoin(BASE_URL, href)
            for href in response.css("div.mw-parser-output a::attr(href)").getall()
            if href.startswith("/wiki/") and ":" not in href  # Avoid special pages
        ]

        # Create a structured Scrapy item and send it to pipeline
        yield WikiPageItem(
            title=title, url=page_url, content=content, categories=categories, links=links
        )

        # Follow links only if they haven’t been visited
        for link in links:
            if link not in self.visited_pages:
                yield response.follow(link, callback=self.parse)
