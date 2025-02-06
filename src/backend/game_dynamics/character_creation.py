"""Implements character creation logic"""

import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.backend.database.models import Background, Character, CharacterClass, Race
from src.backend.orchestrator.services import LLMService
from src.logger_definition import get_logger

logger = get_logger(__file__)


class CharacterManager:
    """Handles character creation, retrieval, and description for DungeonMind."""

    def __init__(self, db: Session, llm_service: LLMService):
        self.db = db
        self.llm_service = llm_service

    def get_available_options(self):
        """Fetch all available races, classes, and backgrounds from the database."""
        races = [race.name for race in self.db.query(Race).all()]
        classes = [char_class.name for char_class in self.db.query(CharacterClass).all()]
        backgrounds = [background.name for background in self.db.query(Background).all()]
        return races, classes, backgrounds

    def parse_character_from_text(self, user_message: str):
        """
        Uses the LLM to extract character attributes from user input.
        """
        available_races, available_classes, available_backgrounds = self.get_available_options()

        system_prompt = f"""You are an expert in character creation for Dungeons & Dragons.
        Based on the user's message, determine their most likely:
        - Character name
        - Race (Choose from: {', '.join(available_races)})
        - Class (Choose from: {', '.join(available_classes)})
        - Background (Choose from: {', '.join(available_backgrounds)})

        If the input is unclear, use the default: Adventurer Human Ranger Urchin.
        Respond with only a JSON object like this:
        {{
            "name": "Arthur",
            "race": "Elf",
            "class": "Wizard",
            "background": "Sage"
        }}
        """

        response = self.llm_service.generate_one_off_response(system_prompt, user_message)

        try:
            parsed_data = json.loads(response)
            return (
                parsed_data.get("name", "Adventurer"),
                (
                    parsed_data.get("race", "Human")
                    if parsed_data.get("race") in available_races
                    else "Human"
                ),
                (
                    parsed_data.get("class", "Ranger")
                    if parsed_data.get("class") in available_classes
                    else "Ranger"
                ),
                (
                    parsed_data.get("background", "Urchin")
                    if parsed_data.get("background") in available_backgrounds
                    else "Urchin"
                ),
            )
        except json.JSONDecodeError as e:
            logger.error("JSON decoding error in character parsing: %s", e)
        except KeyError as e:
            logger.error("Missing key in LLM response: %s", e)

        # Fallback to default character
        return "Adventurer", "Human", "Ranger", "Urchin"

    def create_character(self, user_message: str):
        """Handles character creation when a player does not already have one."""
        character_name, race_name, class_name, background_name = self.parse_character_from_text(
            user_message
        )

        # Fetch the corresponding database entries
        race = self.db.query(Race).filter(Race.name == race_name).first()
        char_class = self.db.query(CharacterClass).filter(CharacterClass.name == class_name).first()
        background = self.db.query(Background).filter(Background.name == background_name).first()

        if not race or not char_class or not background:
            raise HTTPException(
                status_code=400, detail="Invalid race, class, or background parsed by LLM."
            )

        # Create and save the new character
        character = Character(
            name=character_name,
            race_id=race.id,
            class_id=char_class.id,
            background_id=background.id,
            strength=10 + race.strength_bonus,
            dexterity=10 + race.dexterity_bonus,
            constitution=10 + race.constitution_bonus,
            intelligence=10 + race.intelligence_bonus,
            wisdom=10 + race.wisdom_bonus,
            charisma=10 + race.charisma_bonus,
        )
        self.db.add(character)
        self.db.commit()
        self.db.refresh(character)

        return character, race, char_class, background

    def get_character_summary(self, character, race, char_class, background):
        """Generates a structured character summary for the LLM context."""
        return f"""
        Character: {character.name}
        Race: {race.name if race else 'Unknown'}
        Class: {char_class.name if char_class else 'Unknown'}
        Background: {background.name if background else 'Unknown'}

        Stats:
        - Strength: {character.strength}
        - Dexterity: {character.dexterity}
        - Constitution: {character.constitution}
        - Intelligence: {character.intelligence}
        - Wisdom: {character.wisdom}
        - Charisma: {character.charisma}

        Key Traits:
        {', '.join(race.abilities) if race and race.abilities else "No racial traits."}
        """
