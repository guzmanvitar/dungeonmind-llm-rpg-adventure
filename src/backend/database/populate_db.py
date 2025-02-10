"""Populates game db with core game entities"""

from sqlalchemy.orm import Session

from src.backend.database.config import engine
from src.backend.database.models import Background, CharacterClass, Race

# Create a new database session
session = Session(bind=engine)

# --- Races (Core 5e) ---
races = [
    Race(
        name="Human",
        description="Versatile and ambitious.",
        strength_bonus=1,
        dexterity_bonus=1,
        constitution_bonus=1,
        intelligence_bonus=1,
        wisdom_bonus=1,
        charisma_bonus=1,
        abilities=["Extra Language"],
    ),
    Race(
        name="Elf",
        description="Graceful and keen-eyed.",
        dexterity_bonus=2,
        abilities=["Darkvision", "Keen Senses", "Fey Ancestry", "Trance"],
    ),
    Race(
        name="Dwarf",
        description="Stout and resilient.",
        constitution_bonus=2,
        abilities=["Darkvision", "Dwarven Resilience", "Stonecunning"],
        speed=25,
    ),
    Race(
        name="Halfling",
        description="Small and nimble.",
        dexterity_bonus=2,
        abilities=["Lucky", "Brave", "Halfling Nimbleness"],
        speed=25,
    ),
    Race(
        name="Dragonborn",
        description="Draconic heritage grants powerful abilities.",
        strength_bonus=2,
        charisma_bonus=1,
        abilities=["Draconic Ancestry", "Breath Weapon", "Damage Resistance"],
    ),
    Race(
        name="Gnome",
        description="Curious and inventive.",
        intelligence_bonus=2,
        abilities=["Darkvision", "Gnome Cunning"],
        speed=25,
    ),
    Race(
        name="Half-Elf",
        description="Blends human ambition and elven grace.",
        charisma_bonus=2,
        abilities=["Darkvision", "Fey Ancestry", "Skill Versatility"],
    ),
    Race(
        name="Half-Orc",
        description="Strong and enduring.",
        strength_bonus=2,
        constitution_bonus=1,
        abilities=["Darkvision", "Menacing", "Relentless Endurance", "Savage Attacks"],
    ),
    Race(
        name="Tiefling",
        description="Fiendish ancestry grants infernal powers.",
        intelligence_bonus=1,
        charisma_bonus=2,
        abilities=["Darkvision", "Hellish Resistance", "Infernal Legacy"],
    ),
    Race(
        name="Aasimar",
        description="Blessed with celestial heritage.",
        charisma_bonus=2,
        abilities=["Darkvision", "Celestial Resistance", "Healing Hands", "Light Bearer"],
    ),
    Race(
        name="Goliath",
        description="Mountain-dwelling giants.",
        strength_bonus=2,
        constitution_bonus=1,
        abilities=["Natural Athlete", "Stone's Endurance", "Powerful Build", "Mountain Born"],
    ),
]

# --- Classes (Core 5e) ---
classes = [
    CharacterClass(
        name="Barbarian",
        description="A fierce warrior with rage-fueled might.",
        hit_die=12,
        primary_ability="Strength",
        proficiencies=[
            "Light armor",
            "Medium armor",
            "Shields",
            "Simple weapons",
            "Martial weapons",
        ],
        spellcasting=False,
    ),
    CharacterClass(
        name="Bard",
        description="A performer who weaves magic through words and music.",
        hit_die=8,
        primary_ability="Charisma",
        proficiencies=[
            "Light armor",
            "Simple weapons",
            "Hand crossbows",
            "Longswords",
            "Rapiers",
            "Shortswords",
        ],
        spellcasting=True,
    ),
    CharacterClass(
        name="Cleric",
        description="A divine spellcaster granted power by the gods.",
        hit_die=8,
        primary_ability="Wisdom",
        proficiencies=["Light armor", "Medium armor", "Shields", "Simple weapons"],
        spellcasting=True,
    ),
    CharacterClass(
        name="Druid",
        description="A priest of nature, able to transform into animals.",
        hit_die=8,
        primary_ability="Wisdom",
        proficiencies=[
            "Light armor (non-metal)",
            "Medium armor (non-metal)",
            "Shields (non-metal)",
            "Clubs",
            "Daggers",
            "Quarterstaffs",
            "Scimitars",
            "Sickles",
            "Spears",
        ],
        spellcasting=True,
    ),
    CharacterClass(
        name="Fighter",
        description="A master of weapons and armor.",
        hit_die=10,
        primary_ability="Strength or Dexterity",
        proficiencies=["All armor", "Shields", "Simple weapons", "Martial weapons"],
        spellcasting=False,
    ),
    CharacterClass(
        name="Monk",
        description="A martial artist who harnesses ki energy.",
        hit_die=8,
        primary_ability="Dexterity and Wisdom",
        proficiencies=["Simple weapons", "Shortswords"],
        spellcasting=False,
    ),
    CharacterClass(
        name="Paladin",
        description="A holy knight bound by sacred oaths.",
        hit_die=10,
        primary_ability="Strength and Charisma",
        proficiencies=["All armor", "Shields", "Simple weapons", "Martial weapons"],
        spellcasting=True,
    ),
    CharacterClass(
        name="Ranger",
        description="A hunter and tracker of beasts and foes.",
        hit_die=10,
        primary_ability="Dexterity and Wisdom",
        proficiencies=[
            "Light armor",
            "Medium armor",
            "Shields",
            "Simple weapons",
            "Martial weapons",
        ],
        spellcasting=True,
    ),
    CharacterClass(
        name="Rogue",
        description="A stealthy character skilled in deception and precision strikes.",
        hit_die=8,
        primary_ability="Dexterity",
        proficiencies=[
            "Light armor",
            "Simple weapons",
            "Hand crossbows",
            "Longswords",
            "Rapiers",
            "Shortswords",
            "Thieves' tools",
        ],
        spellcasting=False,
    ),
    CharacterClass(
        name="Sorcerer",
        description="A spellcaster whose magic is innate.",
        hit_die=6,
        primary_ability="Charisma",
        proficiencies=["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
        spellcasting=True,
    ),
    CharacterClass(
        name="Warlock",
        description="A spellcaster who gains power from a pact with a supernatural being.",
        hit_die=8,
        primary_ability="Charisma",
        proficiencies=["Light armor", "Simple weapons"],
        spellcasting=True,
    ),
    CharacterClass(
        name="Wizard",
        description="A learned spellcaster who manipulates arcane energies.",
        hit_die=6,
        primary_ability="Intelligence",
        proficiencies=["Daggers", "Quarterstaffs", "Light crossbows"],
        spellcasting=True,
    ),
]

# --- Backgrounds (Core 5e) ---
backgrounds = [
    Background(
        name="Soldier",
        description="A battle-tested warrior.",
        starting_proficiencies=["Athletics", "Intimidation"],
        starting_equipment=["Insignia of rank", "Trophy from fallen enemy", "Belt pouch (10gp)"],
    ),
    Background(
        name="Sage",
        description="A scholar who studies ancient texts.",
        starting_proficiencies=["Arcana", "History"],
        starting_equipment=[
            "Bottle of ink",
            "Quill",
            "Small knife",
            "Letter from a dead colleague",
        ],
    ),
    Background(
        name="Urchin",
        description="A survivor of the streets, skilled in cunning and deception.",
        starting_proficiencies=["Stealth", "Sleight of Hand"],
        starting_equipment=["Small knife", "Pet mouse", "City map", "Belt pouch (10gp)"],
    ),
]

# --- Insert Data into Database ---
session.add_all(races + classes + backgrounds)
session.commit()
print("✅ Database successfully populated with full D&D 5e race, class, and background data!")

# Close the session
session.close()
