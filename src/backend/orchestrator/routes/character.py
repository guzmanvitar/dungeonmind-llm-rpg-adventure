"""Character creation endpoint configuration"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.backend.database.config import SessionLocal
from src.backend.database.models import Background, Character, CharacterClass, Race

router = APIRouter()

# Default character settings
DEFAULT_RACE = "Human"
DEFAULT_CLASS = "Ranger"
DEFAULT_BACKGROUND = "Folk Hero"


def get_db():
    """Dependency to get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/character")
def get_character(db: Session = Depends(get_db)):
    """Returns the character sheet details."""
    character = db.query(Character).first()
    if not character:
        raise HTTPException(status_code=404, detail="No character found")

    # Fetch related class, race, and background details
    race = db.query(Race).filter(Race.id == character.race_id).first()
    char_class = db.query(CharacterClass).filter(CharacterClass.id == character.class_id).first()
    background = db.query(Background).filter(Background.id == character.background_id).first()

    # Fetch racial traits
    traits = [trait.name for trait in race.traits] if race and race.traits else []

    # Fetch saving throws
    saving_throws = char_class.saving_throws if char_class and char_class.saving_throws else []

    # Fetch proficiencies from class and background
    class_proficiencies = (
        [prof.name for prof in char_class.proficiencies]
        if char_class and char_class.proficiencies
        else []
    )
    background_proficiencies = (
        [prof.name for prof in background.starting_proficiencies]
        if background and background.starting_proficiencies
        else []
    )

    # Combine all proficiencies, removing duplicates
    all_proficiencies = sorted(set(class_proficiencies + background_proficiencies))

    # Fetch inventory items
    inventory_list = [item.name for item in character.inventory] if character.inventory else []

    return {
        "name": character.name,
        "race": race.name if race else "Unknown",
        "class": char_class.name if char_class else "Unknown",
        "background": background.name if background else "Unknown",
        "current_hit_points": character.current_hit_points,
        "armor_class": character.armor_class,
        "gold": character.gold,
        "traits": traits,
        "strength": character.strength,
        "dexterity": character.dexterity,
        "constitution": character.constitution,
        "intelligence": character.intelligence,
        "wisdom": character.wisdom,
        "charisma": character.charisma,
        "saving_throws": saving_throws,
        "proficiencies": all_proficiencies,
        "inventory": inventory_list,
    }
