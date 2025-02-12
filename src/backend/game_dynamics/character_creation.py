"""Implements character creation logic"""

import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.backend.database.models import (
    Background,
    Character,
    CharacterClass,
    Equipment,
    Race,
)
from src.backend.orchestrator.services import LLMService
from src.logger_definition import get_logger
from src.utils import weighted_random_stat

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

        # Calculate initial HP: Hit Die + Constitution modifier
        constitution_score = weighted_random_stat() + race.constitution_bonus
        constitution_modifier = (constitution_score - 10) // 2
        initial_hp = char_class.hit_die + constitution_modifier

        # Ensure HP is at least 1
        initial_hp = max(initial_hp, 1)

        # Set starting gold based on background
        starting_gold = background.starting_gold if background.starting_gold else 0.0

        # Get starting inventory from class and background (Querying Equipment objects)
        class_equipment = (
            self.db.query(Equipment)
            .filter(Equipment.id.in_([item.id for item in char_class.starting_equipment]))
            .all()
            if char_class.starting_equipment
            else []
        )
        background_equipment = (
            self.db.query(Equipment)
            .filter(Equipment.id.in_([item.id for item in background.starting_equipment]))
            .all()
            if background.starting_equipment
            else []
        )

        # Combine inventory (remove duplicates by converting to a set and back to a list)
        starting_inventory = list(set(class_equipment + background_equipment))

        # Calculate Dexterity and Wisdom Modifiers
        dexterity_score = weighted_random_stat() + race.dexterity_bonus
        dexterity_modifier = (dexterity_score - 10) // 2

        wisdom_score = weighted_random_stat() + race.wisdom_bonus
        wisdom_modifier = (wisdom_score - 10) // 2

        # Determine Armor Class (AC)
        armor_items = [item for item in starting_inventory if item.category == "Armor"]
        shield_equipped = any(item.name == "Shield" for item in starting_inventory)

        if armor_items:
            # If wearing armor, use its base AC + Dexterity (if applicable)
            worn_armor = max(armor_items, key=lambda x: x.armor_class)  # Pick the highest AC armor
            armor_ac = worn_armor.armor_class

            # Apply Dexterity modifier if armor allows it
            if worn_armor.category == "Light Armor":
                armor_ac += dexterity_modifier
            elif worn_armor.category == "Medium Armor":
                armor_ac += min(dexterity_modifier, 2)  # Medium Armor limits Dex to +2

        elif char_class.name == "Barbarian":
            # Barbarian Unarmored Defense: 10 + Dex Mod + Con Mod
            armor_ac = 10 + dexterity_modifier + constitution_modifier

        elif char_class.name == "Monk":
            # Monk Unarmored Defense: 10 + Dex Mod + Wis Mod
            armor_ac = 10 + dexterity_modifier + wisdom_modifier

        else:
            # Default AC for unarmored characters
            armor_ac = 10 + dexterity_modifier

        # Add +2 AC if character has a shield
        if shield_equipped:
            armor_ac += 2

        # Create and save the new character
        character = Character(
            name=character_name,
            race_id=race.id,
            class_id=char_class.id,
            background_id=background.id,
            current_hit_points=initial_hp,
            armor_class=armor_ac,
            gold=starting_gold,
            strength=weighted_random_stat() + race.strength_bonus,
            dexterity=dexterity_score,
            constitution=constitution_score,
            intelligence=weighted_random_stat() + race.intelligence_bonus,
            wisdom=wisdom_score,
            charisma=weighted_random_stat() + race.charisma_bonus,
            inventory=starting_inventory,
        )

        self.db.add(character)
        self.db.commit()
        self.db.refresh(character)

        return character, race, char_class, background

    def get_character_summary(self, character, race, char_class, background):
        """Generates a structured character summary for the LLM context."""

        # Fetch traits from race
        traits_list = (
            ", ".join([trait.name for trait in race.traits]) if race.traits else "No racial traits"
        )

        # Fetch saving throws from class
        saving_throws = ", ".join(char_class.saving_throws) if char_class.saving_throws else "None"

        # Fetch proficiencies from class and background
        class_proficiencies = (
            [prof.name for prof in char_class.proficiencies] if char_class.proficiencies else []
        )
        background_proficiencies = (
            [prof.name for prof in background.starting_proficiencies]
            if background.starting_proficiencies
            else []
        )

        # Combine class and background proficiencies, removing duplicates
        all_proficiencies = sorted(set(class_proficiencies + background_proficiencies))
        proficiencies_list = ", ".join(all_proficiencies) if all_proficiencies else "None"

        # Extract inventory items
        inventory_list = (
            ", ".join([item.name for item in character.inventory])
            if character.inventory
            else "None"
        )

        return f"""
        Character: {character.name}
        Race: {race.name if race else 'Unknown'}
        Class: {char_class.name if char_class else 'Unknown'}
        Background: {background.name if background else 'Unknown'}

        **Current HP:** {character.current_hit_points}
        **Armor Class (AC):** {character.armor_class}
        **Gold:** {character.gold} GP

        Key Traits:
        {traits_list}

        Stats:
        - Strength: {character.strength}
        - Dexterity: {character.dexterity}
        - Constitution: {character.constitution}
        - Intelligence: {character.intelligence}
        - Wisdom: {character.wisdom}
        - Charisma: {character.charisma}

        Saving Throws:
        {saving_throws}

        Proficiencies:
        {proficiencies_list}

        Inventory:
        {inventory_list}
        """
