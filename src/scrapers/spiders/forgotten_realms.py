"""Forgotten Realms Lore Scraper"""

from urllib.parse import urljoin

import scrapy
from bs4 import BeautifulSoup

from src.scrapers.items import WikiPageItem

BASE_URL = "https://forgottenrealms.fandom.com"


class ForgottenRealmsSpider(scrapy.Spider):
    name = "forgotten_realms"
    allowed_domains = ["forgottenrealms.fandom.com"]
    start_urls = [urljoin(BASE_URL, "/wiki/Abeir-Toril")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited_pages = set()

    def parse(self, response):
        """Extracts page content and links, yielding structured data."""
        page_url = response.url.split("?")[0]

        # Avoid duplicate processing
        if page_url in self.visited_pages:
            return  # Stop processing if we've already visited this page
        self.visited_pages.add(page_url)

        # Extract title
        title = response.css("#firstHeading > span::text").get()
        title = title.strip() if title else "Unknown"

        # Extract full paragraph content, including inline elements
        paragraphs = response.css("div.mw-parser-output p").getall()

        # Use BeautifulSoup to preserve inline links and spans
        cleaned_paragraphs = []
        for paragraph in paragraphs:
            soup = BeautifulSoup(paragraph, "html.parser")
            text = soup.get_text(" ", strip=True)
            cleaned_paragraphs.append(text)

        # Join paragraphs into a single text block
        content = " ".join(cleaned_paragraphs)

        # Extract categories
        categories = response.css(".page-header__categories-in + a::text").getall()
        categories = categories if categories else ["Uncategorized"]

        # Extract all links, filtering out unwanted ones
        links = [
            urljoin(BASE_URL, href.split("?")[0])
            for href in response.css("div.mw-parser-output a::attr(href)").getall()
            if href.startswith("/wiki/")
            and ":" not in href  # Avoid special pages
            and "#cite_note" not in href  # Exclude citation links
        ]

        # Remove links inside the "References" section
        reference_section = (
            response.css("span.mw-headline#References")
            .xpath("following-sibling::ul[1]//a/@href")
            .getall()
        )
        reference_links = {urljoin(BASE_URL, ref.split("?")[0]) for ref in reference_section}
        links = {link for link in links if link not in reference_links}

        # Create a structured Scrapy item and send it to pipeline
        yield WikiPageItem(
            title=title, url=page_url, content=content, categories=categories, links=links
        )

        # Follow links only if they haven’t been visited
        for link in links:
            if link not in self.visited_pages:
                yield response.follow(link, callback=self.parse)
