"""Character creation endpoint configuration"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.backend.database.config import SessionLocal
from src.backend.database.models import Background, Character, CharacterClass, Race

router = APIRouter()

# Default character settings
DEFAULT_RACE = "Human"
DEFAULT_CLASS = "Ranger"
DEFAULT_BACKGROUND = "Urchin"


def get_db():
    """Dependency to get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/character")
def create_character(
    name: str,
    race: str | None = None,
    char_class: str | None = None,
    background: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Creates a new character. If no race, class, or background is specified, defaults to:
    - Race: Human
    - Class: Ranger
    - Background: Urchin
    """
    # Apply default values if missing
    race_name = race or DEFAULT_RACE
    class_name = char_class or DEFAULT_CLASS
    background_name = background or DEFAULT_BACKGROUND

    # Fetch race, class, and background from the database
    race_obj = db.query(Race).filter(Race.name == race_name).first()
    class_obj = db.query(CharacterClass).filter(CharacterClass.name == class_name).first()
    background_obj = db.query(Background).filter(Background.name == background_name).first()

    # Validate if the selections exist in the database
    if not race_obj or not class_obj or not background_obj:
        raise HTTPException(status_code=400, detail="Invalid race, class, or background selection.")

    # Create character with default or provided values
    new_character = Character(
        name=name,
        race_id=race_obj.id,
        class_id=class_obj.id,
        background_id=background_obj.id,
        strength=10 + race_obj.strength_bonus,
        dexterity=10 + race_obj.dexterity_bonus,
        constitution=10 + race_obj.constitution_bonus,
        intelligence=10 + race_obj.intelligence_bonus,
        wisdom=10 + race_obj.wisdom_bonus,
        charisma=10 + race_obj.charisma_bonus,
    )

    db.add(new_character)
    db.commit()
    db.refresh(new_character)

    return {
        "message": "Character created successfully",
        "character": {
            "name": new_character.name,
            "race": race_obj.name,
            "class": class_obj.name,
            "background": background_obj.name,
            "stats": {
                "Strength": new_character.strength,
                "Dexterity": new_character.dexterity,
                "Constitution": new_character.constitution,
                "Intelligence": new_character.intelligence,
                "Wisdom": new_character.wisdom,
                "Charisma": new_character.charisma,
            },
        },
    }


@router.get("/character")
def get_character(db: Session = Depends(get_db)):
    """Returns the character sheet details."""
    character = db.query(Character).first()
    if not character:
        raise HTTPException(status_code=404, detail="No character found")

    race = db.query(Race).filter(Race.id == character.race_id).first()
    char_class = db.query(CharacterClass).filter(CharacterClass.id == character.class_id).first()
    background = db.query(Background).filter(Background.id == character.background_id).first()

    return {
        "name": character.name,
        "race": race.name if race else "Unknown",
        "class": char_class.name if char_class else "Unknown",
        "background": background.name if background else "Unknown",
        "strength": character.strength,
        "dexterity": character.dexterity,
        "constitution": character.constitution,
        "intelligence": character.intelligence,
        "wisdom": character.wisdom,
        "charisma": character.charisma,
    }
