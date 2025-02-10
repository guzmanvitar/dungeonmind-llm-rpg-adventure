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
        saving_throws=["Strength", "Constitution"],
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
        saving_throws=["Dexterity", "Charisma"],
    ),
    CharacterClass(
        name="Cleric",
        description="A divine spellcaster granted power by the gods.",
        hit_die=8,
        primary_ability="Wisdom",
        proficiencies=["Light armor", "Medium armor", "Shields", "Simple weapons"],
        spellcasting=True,
        saving_throws=["Wisdom", "Charisma"],
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
        saving_throws=["Intelligence", "Wisdom"],
    ),
    CharacterClass(
        name="Fighter",
        description="A master of weapons and armor.",
        hit_die=10,
        primary_ability="Strength or Dexterity",
        proficiencies=["All armor", "Shields", "Simple weapons", "Martial weapons"],
        spellcasting=False,
        saving_throws=["Strength", "Constitution"],
    ),
    CharacterClass(
        name="Monk",
        description="A martial artist who harnesses ki energy.",
        hit_die=8,
        primary_ability="Dexterity and Wisdom",
        proficiencies=["Simple weapons", "Shortswords"],
        spellcasting=False,
        saving_throws=["Strength", "Dexterity"],
    ),
    CharacterClass(
        name="Paladin",
        description="A holy knight bound by sacred oaths.",
        hit_die=10,
        primary_ability="Strength and Charisma",
        proficiencies=["All armor", "Shields", "Simple weapons", "Martial weapons"],
        spellcasting=True,
        saving_throws=["Wisdom", "Charisma"],
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
        saving_throws=["Strength", "Dexterity"],
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
        saving_throws=["Dexterity", "Intelligence"],
    ),
    CharacterClass(
        name="Sorcerer",
        description="A spellcaster whose magic is innate.",
        hit_die=6,
        primary_ability="Charisma",
        proficiencies=["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
        spellcasting=True,
        saving_throws=["Constitution", "Charisma"],
    ),
    CharacterClass(
        name="Warlock",
        description="A spellcaster who gains power from a pact with a supernatural being.",
        hit_die=8,
        primary_ability="Charisma",
        proficiencies=["Light armor", "Simple weapons"],
        spellcasting=True,
        saving_throws=["Wisdom", "Charisma"],
    ),
    CharacterClass(
        name="Wizard",
        description="A learned spellcaster who manipulates arcane energies.",
        hit_die=6,
        primary_ability="Intelligence",
        proficiencies=["Daggers", "Quarterstaffs", "Light crossbows"],
        spellcasting=True,
        saving_throws=["Intelligence", "Wisdom"],
    ),
]
# --- Backgrounds (Core 5e) ---
backgrounds = [
    Background(
        name="Acolyte",
        description="You have spent your life in the service of a temple to a specific god or"
        " pantheon.",
        starting_proficiencies=["Insight", "Religion"],
        starting_equipment=[
            "Holy symbol",
            "Prayer book or prayer wheel",
            "5 sticks of incense",
            "Vestments",
            "Set of common clothes",
            "Belt pouch containing 15 gp",
        ],
    ),
    Background(
        name="Charlatan",
        description="You have always had a way with people, and you know how to make them trust "
        "you.",
        starting_proficiencies=["Deception", "Sleight of Hand"],
        starting_equipment=[
            "Set of fine clothes",
            "Disguise kit",
            "Tools of the con (ten stoppered bottles filled with colored liquid, set of weighted"
            " dice, deck of marked cards, or signet ring of an imaginary duke)",
            "Belt pouch containing 15 gp",
        ],
    ),
    Background(
        name="Criminal",
        description="You are an experienced criminal with a history of breaking the law.",
        starting_proficiencies=["Deception", "Stealth"],
        starting_equipment=[
            "Crowbar",
            "Set of dark common clothes including a hood",
            "Belt pouch containing 15 gp",
        ],
    ),
    Background(
        name="Entertainer",
        description="You thrive in front of an audience, making the world your stage.",
        starting_proficiencies=["Acrobatics", "Performance"],
        starting_equipment=[
            "Musical instrument (one of your choice)",
            "The favor of an admirer (love letter, lock of hair, or trinket)",
            "Costume",
            "Belt pouch containing 15 gp",
        ],
    ),
    Background(
        name="Folk Hero",
        description="You come from a humble social rank, but you are destined for so much more.",
        starting_proficiencies=["Animal Handling", "Survival"],
        starting_equipment=[
            "Set of artisan's tools (one of your choice)",
            "Shovel",
            "Iron pot",
            "Set of common clothes",
            "Belt pouch containing 10 gp",
        ],
    ),
    Background(
        name="Guild Artisan",
        description="You are a member of an artisan's guild, skilled in a particular field and"
        " closely associated with other artisans.",
        starting_proficiencies=["Insight", "Persuasion"],
        starting_equipment=[
            "Set of artisan's tools (one of your choice)",
            "Letter of introduction from your guild",
            "Set of traveler's clothes",
            "Belt pouch containing 15 gp",
        ],
    ),
    Background(
        name="Hermit",
        description="You lived in seclusion, either in a sheltered community or entirely alone.",
        starting_proficiencies=["Medicine", "Religion"],
        starting_equipment=[
            "Scroll case stuffed full of notes from your studies or prayers",
            "Winter blanket",
            "Set of common clothes",
            "Herbalism kit",
            "5 gp",
        ],
    ),
    Background(
        name="Noble",
        description="You understand wealth, power, and privilege.",
        starting_proficiencies=["History", "Persuasion"],
        starting_equipment=[
            "Set of fine clothes",
            "Signet ring",
            "Scroll of pedigree",
            "Purse containing 25 gp",
        ],
    ),
    Background(
        name="Outlander",
        description="You grew up in the wilds, far from civilization and the comforts of town and"
        " technology.",
        starting_proficiencies=["Athletics", "Survival"],
        starting_equipment=[
            "Staff",
            "Hunting trap",
            "Trophy from an animal you killed",
            "Set of traveler's clothes",
            "Belt pouch containing 10 gp",
        ],
    ),
    Background(
        name="Sage",
        description="You spent years learning the lore of the multiverse.",
        starting_proficiencies=["Arcana", "History"],
        starting_equipment=[
            "Bottle of black ink",
            "Quill",
            "Small knife",
            "Letter from a dead colleague posing a question you have not yet been able to answer",
            "Set of common clothes",
            "Belt pouch containing 10 gp",
        ],
    ),
    Background(
        name="Sailor",
        description="You sailed on a seagoing vessel for years.",
        starting_proficiencies=["Athletics", "Perception"],
        starting_equipment=[
            "Belaying pin (club)",
            "50 feet of silk rope",
            "Lucky charm such as a rabbit foot or a small stone with a hole in the center",
            "Set of common clothes",
            "Belt pouch containing 10 gp",
        ],
    ),
    Background(
        name="Soldier",
        description="You are a battle-tested warrior.",
        starting_proficiencies=["Athletics", "Intimidation"],
        starting_equipment=[
            "Insignia of rank",
            "Trophy from a fallen enemy (a dagger, broken blade, or piece of a banner)",
            "Set of bone dice or deck of cards",
            "Set of common clothes",
            "Belt pouch containing 10 gp",
        ],
    ),
    Background(
        name="Urchin",
        description="You grew up on the streets alone, orphaned, and poor.",
        starting_proficiencies=["Sleight of Hand", "Stealth"],
        starting_equipment=[
            "Small knife",
            "Map of the city you grew up in",
            "Pet mouse",
            "Token to remember your parents by",
            "Set of common clothes",
            "Belt pouch containing 10 gp",
        ],
    ),
]

# --- Insert Data into Database ---
session.add_all(races + classes + backgrounds)
session.commit()
print("✅ Database successfully populated with full D&D 5e race, class, and background data!")

# Close the session
session.close()
