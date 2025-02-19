"""Implements campaign creation logic"""

import random

import networkx as nx
from langchain_community.vectorstores import FAISS

from src.backend.orchestrator.services import LLMServiceFactory
from src.constants import DATABASE, DATABASE_FAISS
from src.logger_definition import get_logger

logger = get_logger(__file__)


class CampaignManager:
    """
    Service for generating a complete Dungeons & Dragons one-shot campaign in the Forgotten Realms.

    This class selects a campaign setting, retrieves relevant world elements, and generates a fully
    formatted adventure using GPT-4, structured according to a D&D module format.

    Dependencies:
        - FAISS: Vector search for retrieving locations, characters, creatures, items, and lore.
        - NetworkX: Knowledge graph (`forgotten_realms_graph.gml`) for hierarchical world navigation

    Attributes:
        location_service (LLMService): LLM for selecting adventure locations.
        campaign_creation_service (LLMService): LLM for generating the final campaign.
        embedding_model (OpenAIEmbeddings): Embedding model for FAISS vector search.
        wiki_graph (networkx.DiGraph): Knowledge graph of Forgotten Realms locations.
        FAISS databases (FAISS): Stores locations, characters, creatures, items, and historical lore

    Methods:
        select_campaign_location(user_input: str) -> dict
            Finds the most thematically appropriate Forgotten Realms setting for the adventure.
        select_campaign_elements(selected_location: str, location_summary: str) -> dict
            Retrieves 10 characters, 10 creatures, 10 items, and 20 historical/cultural facts.
        generate_campaign(user_input: str) -> dict
            Calls the above methods and generates a fully formatted adventure using GPT-4.
    """

    def __init__(self):
        """Initializes FAISS retrievers and OpenAI LLM service."""
        self.location_service = LLMServiceFactory("gpt3-5", "location-selection").get_service()
        self.campaign_creation_service = LLMServiceFactory(
            "gpt-4", "campaign-creation"
        ).get_service()

        self.embedding_model = self.location_service.embedding_model

        # Load FAISS vector databases
        self.places_db = FAISS.load_local(
            str(DATABASE_FAISS / "places"),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )
        self.history_db = FAISS.load_local(
            str(DATABASE_FAISS / "history_and_culture"),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )
        self.characters_db = FAISS.load_local(
            str(DATABASE_FAISS / "characters"),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )
        self.creatures_db = FAISS.load_local(
            str(DATABASE_FAISS / "creatures"),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )
        self.items_db = FAISS.load_local(
            str(DATABASE_FAISS / "items"),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )

        # Load the NetworkX knowledge graph
        self.wiki_graph = self._load_graph()

    def _load_graph(self):
        """Loads the knowledge graph from the stored .gml file."""
        graph_path = DATABASE / "forgotten_realms_graph.gml"
        if graph_path.exists():
            return nx.read_gml(graph_path)
        else:
            logger.warning("Knowledge graph not found. Some features may be unavailable.")
            return nx.DiGraph()  # Return an empty graph if the file is missing

    def get_hierarchical_location(self, selected_location: str):
        """Finds the hierarchical path from a specific location up to its broadest category.

        - First, moves up until finding the **first Region or Country**.
        - Then, continues moving up until finding a **Continent**.
        """
        # TODO: Improve logic for higher match rate
        # Convert selected title to its expected wiki URL format
        wiki_url = f"https://forgottenrealms.fandom.com/wiki/{selected_location.replace(' ', '_')}"

        if wiki_url not in self.wiki_graph:
            return []  # No matching node found

        hierarchy = []
        current_node = wiki_url

        # First loop: Find the first "Region" or "Country"
        while True:
            parents = list(self.wiki_graph.predecessors(current_node))  # Get parent nodes

            region_or_country_parents = [
                parent
                for parent in parents
                if any(
                    category in self.wiki_graph.nodes[parent].get("categories", "")
                    for category in ["Regions", "Countries"]
                )
            ]

            if not region_or_country_parents:
                break  # Stop if no "Region" or "Country" is found

            parent = region_or_country_parents[0]  # Take the first matching parent
            hierarchy.append(parent)
            current_node = parent  # Move up to the next level

        # Second loop: Find the first "Continent"
        while True:
            parents = list(self.wiki_graph.predecessors(current_node))  # Get parent nodes

            continent_parents = [
                parent
                for parent in parents
                if "Continents" in self.wiki_graph.nodes[parent].get("categories", "")
            ]

            if not continent_parents:
                break  # Stop if no more continents exist

            parent = continent_parents[0]
            hierarchy.append(parent)
            current_node = parent  # Move up to the next level

        return hierarchy[::-1]  # Return from broad to specific

    def select_campaign_location(self, user_input: str):
        """Generates the campaign starting location based on user input using an LLM-powered FAISS
        search.
        """

        # Retrieve 20 relevant locations from FAISS
        retrieved_docs = self.places_db.similarity_search(user_input, k=20)

        if not retrieved_docs:
            return {"error": "No suitable locations found."}

        # Randomly select 10 locations for variety
        selected_docs = random.sample(retrieved_docs, min(10, len(retrieved_docs)))

        # Prepare list of retrieved locations
        location_options = [
            f"- {doc.metadata.get('title', 'Unknown')}: {doc.page_content[:300]}..."
            for doc in selected_docs
        ]

        # Construct LLM prompt to pick the best specific location
        location_list = "\n".join(location_options)

        if not self.location_service.initial_prompt:
            raise ValueError("Missing system prompt for location service")

        location_prompt = self.location_service.initial_prompt.format(
            location_list=location_list, user_input=user_input
        )

        chosen_location = self.location_service.generate_formatted_response(location_prompt).strip()
        location_description = [
            location.page_content
            for location in selected_docs
            if location.metadata.get("title") == chosen_location
        ][0]

        # Get a location summary from full description of selected location
        location_summary = self.location_service.generate_formatted_response(
            "Create a summarized version of the following fantasy location wiki:"
            f" {location_description}"
        )

        # Retrieve hierarchical location breakdown
        location_hierarchy = self.get_hierarchical_location(chosen_location)

        return {
            "selected_location": chosen_location,
            "location_description": location_description,
            "location_summary": location_summary,
            "location_hierarchy": location_hierarchy,
        }

    def select_campaign_elements(self, selected_location: str, location_summary: str):
        """
        Fetches a list of related characters, creatures, items, and historical/cultural facts
        for the given location. Constructs a structured adventure context summary.
        """

        # Use both the location name and summary in FAISS searches
        search_query = f"{selected_location}: {location_summary}"

        # Retrieve 15 candidates for each category
        characters = self.characters_db.similarity_search(search_query, k=15)
        creatures = self.creatures_db.similarity_search(search_query, k=15)
        items = self.items_db.similarity_search(search_query, k=15)
        cultural_facts = self.history_db.similarity_search(search_query, k=50)

        # Randomly select the required number from candidates
        selected_characters = random.sample(characters, min(10, len(characters)))
        selected_creatures = random.sample(creatures, min(10, len(creatures)))
        selected_items = random.sample(items, min(10, len(items)))
        selected_cultural_facts = random.sample(cultural_facts, min(20, len(cultural_facts)))

        # Extract metadata for final selection
        character_list = [char.metadata.get("title", "Unknown") for char in selected_characters]
        creature_list = [
            creature.metadata.get("title", "Unknown") for creature in selected_creatures
        ]
        item_list = [item.metadata.get("title", "Unknown") for item in selected_items]
        cultural_fact_list = [
            fact.page_content[:300] for fact in selected_cultural_facts
        ]  # Trim for clarity

        # Build a structured summary
        adventure_context = {
            "selected_location": selected_location,
            "location_summary": location_summary,
            "characters": character_list,
            "creatures": creature_list,
            "items": item_list,
            "cultural_facts": cultural_fact_list,
        }

        return adventure_context

    def generate_campaign(self, user_input: str) -> str:
        """
        Generates a full D&D one-shot campaign from scratch using user input.

        This method:
        - Selects an appropriate Forgotten Realms location.
        - Retrieves relevant characters, creatures, items, and lore.
        - Calls GPT-4 to generate a complete campaign based on the D&D One-Shot Template.

        Args:
            user_input (str): A brief description of the type of adventure the user wants.

        Returns:
            str: The generated campaign text.
        """
        # Select the campaign location
        location_output = self.select_campaign_location(user_input)

        # Retrieve campaign elements (characters, creatures, items, lore)
        campaign_elements = self.select_campaign_elements(
            location_output["selected_location"], location_output["location_summary"]
        )

        if not self.campaign_creation_service.initial_prompt:
            raise ValueError("Missing system prompt for campaign creation service")

        campaign_creation_prompt = self.campaign_creation_service.initial_prompt.format(
            selected_location=campaign_elements["selected_location"],
            location_summary=campaign_elements["location_summary"],
            characters=", ".join(campaign_elements["characters"]),
            creatures=", ".join(campaign_elements["creatures"]),
            items=", ".join(campaign_elements["items"]),
            cultural_facts=", ".join(campaign_elements["cultural_facts"]),
        )

        return self.campaign_creation_service.generate_formatted_response(campaign_creation_prompt)
