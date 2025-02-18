# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
import os

import networkx as nx
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from src.constants import DATABASE, SECRETS
from src.scrapers.items import WikiPageItem

# Paths for saving databases
GRAPH_SAVE_PATH = DATABASE / "forgotten_realms_graph.gml"
FAISS_DB_PATH = DATABASE / "faiss"

# Category-to-embedding mappings
CATEGORY_MAPPING = {
    "Inhabitants": "Characters",
    "Locations": "Places",
    "Buildings": "Places",
    "Roads": "Places",
    "Items": "Items",
    "Organizations": "History and Culture",
    "Years": "History and Culture",
    "Languages": "History and Culture",
    "Deities": "History and Culture",
    "Vegetation": "History and Culture",
    "Medium-sized creatures": "Creatures",
    "Large creatures": "Creatures",
    "Small creatures": "Creatures",
    "Huge creatures": "Creatures",
    "Tiny creatures": "Creatures",
}


# Load OpenAI API Key
def load_openai_api_key():
    """Load OpenAI API key from environment or .secrets file."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key and SECRETS.exists():
        try:
            with open(SECRETS / "open-ai-creds.json", encoding="utf-8") as f:
                api_key = json.load(f).get("key")
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading OpenAI credentials: {e}") from e

    return api_key


class WikiGraphPipeline:
    """
    A Scrapy pipeline that processes and stores wiki data in a graph and vector database.

    This pipeline performs the following tasks:
    1. Stores extracted wiki pages as nodes in a **NetworkX graph**.
    2. Stores relationships (links between pages) as **edges** in the graph.
    3. Categorizes relevant pages and embeds their content in **FAISS** for fast retrieval.
    4. Saves both the graph (`.gml` format) and FAISS databases when the crawl ends.

    Attributes:
        wiki_graph (networkx.DiGraph): A directed graph storing wiki pages and relationships.
        vector_stores (dict): A dictionary mapping categories to FAISS vector databases.
        embedding_model (OpenAIEmbeddings): The model used to generate text embeddings.
        openai_api_key (str): The API key used for OpenAI embeddings.
    """

    def __init__(self):
        """Initialize an empty NetworkX graph and FAISS vector stores."""
        self.openai_api_key = load_openai_api_key()

        # Initialize networkx
        if GRAPH_SAVE_PATH.exists():
            self.wiki_graph = nx.read_gml(GRAPH_SAVE_PATH)
        else:
            self.wiki_graph = nx.DiGraph()

        # Initialize FAISS databases
        self.vector_stores = {}
        self.embedding_model = OpenAIEmbeddings(
            model="text-embedding-ada-002", openai_api_key=self.openai_api_key
        )

        # Load existing FAISS vector stores (or initialize new ones)
        FAISS_DB_PATH.mkdir(exist_ok=True)
        for category in CATEGORY_MAPPING.values():
            path = FAISS_DB_PATH / category.lower().replace(" ", "_")
            if path.exists():
                print(f"Loading existing FAISS database for {category}...")
                self.vector_stores[category] = FAISS.load_local(str(path), self.embedding_model)
            else:
                print(f"Creating new FAISS database for {category}...")
                self.vector_stores[category] = None  # Will be initialized on first insert

    def open_spider(self, spider):
        """Called when the spider starts."""
        spider.logger.info("🕷️ Scraper started. Building knowledge graph...")

    def close_spider(self, spider):
        """Called when the spider stops. Saves the graph."""
        nx.write_gml(self.wiki_graph, GRAPH_SAVE_PATH)
        spider.logger.info(f"Wiki Graph Saved to {GRAPH_SAVE_PATH}")

        for category, vector_store in self.vector_stores.items():
            if vector_store:
                vector_store.save_local(str(FAISS_DB_PATH / category.lower().replace(" ", "_")))
                spider.logger.info(f"FAISS database saved for {category}")
            else:
                spider.logger.info(f"No vector_store for {category}")

    def process_item(self, item, spider):
        """Processes each wiki page and adds it to the NetworkX graph."""
        if not isinstance(item, WikiPageItem):
            return item  # Skip non-wiki items (if any)

        url = item["url"]
        title = item["title"]
        content = item["content"]
        categories = ", ".join(item["categories"]) if item["categories"] else "Uncategorized"

        # Add node to knowledge graph
        if url not in self.wiki_graph.nodes:
            self.wiki_graph.add_node(
                url, title=title, content=content, categories=", ".join(categories)
            )

        # Add edges (relationships)
        linked_pages = []
        for link in item["links"]:
            if not self.wiki_graph.has_edge(url, link):
                self.wiki_graph.add_edge(url, link)
                linked_pages.append(link)

        # Process relevant categories for embeddings
        relevant_table = None
        for category in categories.split(","):
            if category in CATEGORY_MAPPING:
                relevant_table = CATEGORY_MAPPING[category]
                break  # Assign the first matching category

        if relevant_table:
            # Include graph-based relationships in FAISS metadata
            metadata = {
                "title": title,
                "url": url,
                "linked_pages": linked_pages[:10],  # Store only top 10 related pages
            }

            # Ensure FAISS vector store is initialized
            if self.vector_stores[relevant_table] is None:
                self.vector_stores[relevant_table] = FAISS.from_texts(
                    [content], self.embedding_model, metadatas=[metadata]
                )
            else:
                # Append new embedding
                self.vector_stores[relevant_table].add_texts([content], metadatas=[metadata])

            spider.logger.info(f"Added '{title}' to {relevant_table} embeddings")

        return item
