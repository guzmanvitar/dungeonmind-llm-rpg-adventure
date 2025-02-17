# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import networkx as nx

from src.constants import DATABASE
from src.scrapers.items import WikiPageItem

SAVE_PATH = DATABASE / "forgotten_realms_graph.gml"


class WikiGraphPipeline:
    def __init__(self):
        """Initialize an empty NetworkX graph."""
        self.wiki_graph = nx.DiGraph()

    def open_spider(self, spider):
        """Called when the spider starts."""
        spider.logger.info("🕷️ Scraper started. Building knowledge graph...")

    def close_spider(self, spider):
        """Called when the spider stops. Saves the graph."""
        nx.write_gml(self.wiki_graph, SAVE_PATH)
        spider.logger.info(f"Wiki Graph Saved to {SAVE_PATH}")

    def process_item(self, item, spider):
        """Processes each wiki page and adds it to the NetworkX graph."""
        if not isinstance(item, WikiPageItem):
            return item  # Skip non-wiki items (if any)

        url = item["url"]
        title = item["title"]
        content = item["content"]
        categories = ", ".join(item["categories"]) if item["categories"] else "Uncategorized"

        # Add wiki page as a node
        self.wiki_graph.add_node(url, title=title, content=content, categories=categories)

        # Add relationships (edges)
        for link in item["links"]:
            self.wiki_graph.add_edge(url, link)  # Parent → Child relationship

        return item
