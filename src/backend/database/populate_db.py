"""Populates game db with core game entities"""

from sqlalchemy.orm import Session

from src.backend.database.config import engine
from src.backend.database.models import (
    Background,
    CharacterClass,
    Proficiency,
    Race,
    Trait,
)

# Create a new database session
session = Session(bind=engine)


traits = [
    Trait(
        index="extra-language",
        name="Extra Language",
        description="You can speak, read, and write one additional language of your choice.",
        proficiencies=["One extra language"],
    ),
    Trait(
        index="darkvision",
        name="Darkvision",
        description="You have superior vision in dark and dim conditions. You can see in dim light"
        " within 60 feet of you as if it were bright light, and in darkness as if it were dim"
        " light.",
    ),
    Trait(
        index="keen-senses",
        name="Keen Senses",
        description="You have proficiency in the Perception skill.",
        proficiencies=["Perception"],
    ),
    Trait(
        index="fey-ancestry",
        name="Fey Ancestry",
        description="You have advantage on saving throws against being charmed, and magic cannot"
        " put you to sleep.",
    ),
    Trait(
        index="trance",
        name="Trance",
        description="Elves do not need to sleep. Instead, they meditate deeply, remaining"
        " semiconscious, for 4 hours a day.",
    ),
    Trait(
        index="dwarven-resilience",
        name="Dwarven Resilience",
        description="You have advantage on saving throws against poison, and you have resistance"
        " against poison damage.",
    ),
    Trait(
        index="stonecunning",
        name="Stonecunning",
        description="Whenever you make an Intelligence (History) check related to stonework, you"
        " are considered proficient and add double your proficiency bonus.",
        proficiencies=["History (stonework specialization)"],
    ),
    Trait(
        index="brave",
        name="Brave",
        description="You have advantage on saving throws against being frightened.",
    ),
    Trait(
        index="halfling-nimbleness",
        name="Halfling Nimbleness",
        description="You can move through the space of any creature that is at least one size"
        " larger than you.",
    ),
    Trait(
        index="lucky",
        name="Lucky",
        description="When you roll a 1 on a d20 for an attack roll, ability check, or saving"
        " throw, you can reroll the die and must use the new roll.",
    ),
    Trait(
        index="draconic-ancestry",
        name="Draconic Ancestry",
        description="You have draconic ancestry. Your breath weapon and damage resistance are"
        " determined by your dragon type.",
    ),
    Trait(
        index="breath-weapon",
        name="Breath Weapon",
        description="You can use your action to exhale destructive energy. The size, shape, and"
        " damage type depend on your draconic ancestry.",
    ),
    Trait(
        index="damage-resistance",
        name="Damage Resistance",
        description="You have resistance to the damage type associated with your draconic"
        " ancestry.",
    ),
    Trait(
        index="gnome-cunning",
        name="Gnome Cunning",
        description="You have advantage on all Intelligence, Wisdom, and Charisma saving throws"
        " against magic.",
    ),
    Trait(
        index="skill-versatility",
        name="Skill Versatility",
        description="You gain proficiency in two skills of your choice.",
        proficiencies=["Two skills of your choice"],
    ),
    Trait(
        index="menacing",
        name="Menacing",
        description="You gain proficiency in the Intimidation skill.",
        proficiencies=["Intimidation"],
    ),
    Trait(
        index="relentless-endurance",
        name="Relentless Endurance",
        description="When you are reduced to 0 hit points but not killed outright, you can drop"
        " to 1 hit point instead. This can be used once per long rest.",
    ),
    Trait(
        index="savage-attacks",
        name="Savage Attacks",
        description="When you score a critical hit with a melee weapon attack, you can roll one"
        " additional damage die and add it to the extra damage.",
    ),
    Trait(
        index="hellish-resistance",
        name="Hellish Resistance",
        description="You have resistance to fire damage.",
    ),
    Trait(
        index="infernal-legacy",
        name="Infernal Legacy",
        description="You know the thaumaturgy cantrip. At higher levels, you gain access to more"
        " spells from your fiendish heritage.",
        proficiencies=["Thaumaturgy cantrip"],
    ),
]

# Insert traits into the database
session.add_all(traits)
session.commit()


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
        speed=30,
    ),
    Race(
        name="Elf",
        description="Graceful and keen-eyed.",
        dexterity_bonus=2,
        speed=30,
    ),
    Race(
        name="Dwarf",
        description="Stout and resilient.",
        constitution_bonus=2,
        speed=25,
    ),
    Race(
        name="Halfling",
        description="Small and nimble.",
        dexterity_bonus=2,
        speed=25,
    ),
    Race(
        name="Dragonborn",
        description="Draconic heritage grants powerful traits.",
        strength_bonus=2,
        charisma_bonus=1,
        speed=30,
    ),
    Race(
        name="Gnome",
        description="Curious and inventive.",
        intelligence_bonus=2,
        speed=25,
    ),
    Race(
        name="Half-Elf",
        description="Blends human ambition and elven grace.",
        charisma_bonus=2,
        speed=30,
    ),
    Race(
        name="Half-Orc",
        description="Strong and enduring.",
        strength_bonus=2,
        constitution_bonus=1,
        speed=30,
    ),
    Race(
        name="Tiefling",
        description="Fiendish ancestry grants infernal powers.",
        intelligence_bonus=1,
        charisma_bonus=2,
        speed=30,
    ),
]

# Assign traits to races
race_traits = {
    "Human": ["extra-language"],
    "Elf": ["darkvision", "keen-senses", "fey-ancestry", "trance"],
    "Dwarf": ["darkvision", "dwarven-resilience", "stonecunning"],
    "Halfling": ["brave", "lucky", "halfling-nimbleness"],
    "Dragonborn": ["draconic-ancestry", "breath-weapon", "damage-resistance"],
    "Gnome": ["darkvision", "gnome-cunning"],
    "Half-Elf": ["darkvision", "fey-ancestry", "skill-versatility"],
    "Half-Orc": ["darkvision", "menacing", "relentless-endurance", "savage-attacks"],
    "Tiefling": ["darkvision", "hellish-resistance", "infernal-legacy"],
}

trait_map = {trait.index: trait for trait in session.query(Trait).all()}

for race in races:
    if race.name in race_traits:
        for trait_index in race_traits[race.name]:
            if trait_index in trait_map:
                race.traits.append(trait_map[trait_index])

session.add_all(races)
session.commit()

print("✅ Traits and Races successfully populated with correct mappings!")


# List of proficiencies categorized by type
proficiencies = [
    # Skills
    Proficiency(
        name="Acrobatics",
        category="Skill",
        description="Dexterity-based skill for balancing and tumbling.",
    ),
    Proficiency(
        name="Animal Handling",
        category="Skill",
        description="Wisdom-based skill for handling animals.",
    ),
    Proficiency(
        name="Arcana",
        category="Skill",
        description="Intelligence-based skill for knowledge of magic.",
    ),
    Proficiency(
        name="Athletics",
        category="Skill",
        description="Strength-based skill for climbing, swimming, and jumping.",
    ),
    Proficiency(
        name="Deception",
        category="Skill",
        description="Charisma-based skill for lying and misleading.",
    ),
    Proficiency(
        name="History",
        category="Skill",
        description="Intelligence-based skill for knowledge of historical events.",
    ),
    Proficiency(
        name="Insight",
        category="Skill",
        description="Wisdom-based skill for detecting lies and motives.",
    ),
    Proficiency(
        name="Intimidation",
        category="Skill",
        description="Charisma-based skill for coercing and scaring others.",
    ),
    Proficiency(
        name="Investigation",
        category="Skill",
        description="Intelligence-based skill for finding clues and deducing facts.",
    ),
    Proficiency(
        name="Medicine",
        category="Skill",
        description="Wisdom-based skill for diagnosing and treating ailments.",
    ),
    Proficiency(
        name="Nature",
        category="Skill",
        description="Intelligence-based skill for knowledge of nature.",
    ),
    Proficiency(
        name="Perception",
        category="Skill",
        description="Wisdom-based skill for spotting hidden things.",
    ),
    Proficiency(
        name="Performance",
        category="Skill",
        description="Charisma-based skill for acting, singing, or playing instruments.",
    ),
    Proficiency(
        name="Persuasion",
        category="Skill",
        description="Charisma-based skill for influencing others.",
    ),
    Proficiency(
        name="Religion",
        category="Skill",
        description="Intelligence-based skill for knowledge of deities and religious practices.",
    ),
    Proficiency(
        name="Sleight of Hand",
        category="Skill",
        description="Dexterity-based skill for pickpocketing and trickery.",
    ),
    Proficiency(
        name="Stealth", category="Skill", description="Dexterity-based skill for moving silently."
    ),
    Proficiency(
        name="Survival",
        category="Skill",
        description="Wisdom-based skill for tracking and wilderness survival.",
    ),
    # Tools
    Proficiency(
        name="Alchemist's Supplies",
        category="Tool",
        description="Used for creating potions and alchemical substances.",
    ),
    Proficiency(
        name="Brewer's Supplies",
        category="Tool",
        description="Used for crafting alcoholic beverages.",
    ),
    Proficiency(
        name="Calligrapher's Supplies",
        category="Tool",
        description="Used for elegant handwriting and inscriptions.",
    ),
    Proficiency(
        name="Carpenter's Tools",
        category="Tool",
        description="Used for building wooden structures and objects.",
    ),
    Proficiency(
        name="Cartographer's Tools",
        category="Tool",
        description="Used for making and reading maps.",
    ),
    Proficiency(
        name="Cobbler's Tools", category="Tool", description="Used for making and repairing shoes."
    ),
    Proficiency(name="Cook's Utensils", category="Tool", description="Used for preparing meals."),
    Proficiency(
        name="Glassblower's Tools", category="Tool", description="Used for crafting glass objects."
    ),
    Proficiency(
        name="Jeweler's Tools",
        category="Tool",
        description="Used for crafting and appraising jewelry.",
    ),
    Proficiency(
        name="Leatherworker's Tools", category="Tool", description="Used for making leather goods."
    ),
    Proficiency(name="Mason's Tools", category="Tool", description="Used for working with stone."),
    Proficiency(
        name="Painter's Supplies",
        category="Tool",
        description="Used for painting and artistic expression.",
    ),
    Proficiency(
        name="Potter's Tools", category="Tool", description="Used for making ceramic objects."
    ),
    Proficiency(
        name="Smith's Tools",
        category="Tool",
        description="Used for forging and repairing metal objects.",
    ),
    Proficiency(
        name="Tinker's Tools",
        category="Tool",
        description="Used for crafting and repairing mechanical devices.",
    ),
    Proficiency(name="Weaver's Tools", category="Tool", description="Used for weaving textiles."),
    Proficiency(
        name="Woodcarver's Tools", category="Tool", description="Used for carving wooden objects."
    ),
    Proficiency(name="Disguise Kit", category="Tool", description="Used for creating disguises."),
    Proficiency(name="Forgery Kit", category="Tool", description="Used for faking documents."),
    Proficiency(
        name="Herbalism Kit",
        category="Tool",
        description="Used for creating herbal remedies and poisons.",
    ),
    Proficiency(
        name="Navigator's Tools",
        category="Tool",
        description="Used for navigation and map-reading.",
    ),
    Proficiency(
        name="Poisoner's Kit",
        category="Tool",
        description="Used for crafting and handling poisons.",
    ),
    Proficiency(
        name="Thieves' Tools",
        category="Tool",
        description="Used for lockpicking and disabling traps.",
    ),
    Proficiency(
        name="Vehicles (Land)",
        category="Tool",
        description="Proficiency in operating land vehicles.",
    ),
    Proficiency(
        name="Vehicles (Water)",
        category="Tool",
        description="Proficiency in operating water vehicles.",
    ),
    # Musical Instruments
    Proficiency(
        name="Bagpipes", category="Tool", description="A wind instrument with a distinctive sound."
    ),
    Proficiency(
        name="Drum", category="Tool", description="A percussion instrument used for rhythm."
    ),
    Proficiency(
        name="Dulcimer",
        category="Tool",
        description="A string instrument played by striking the strings.",
    ),
    Proficiency(name="Flute", category="Tool", description="A woodwind instrument."),
    Proficiency(name="Lute", category="Tool", description="A plucked string instrument."),
    Proficiency(name="Lyre", category="Tool", description="A small harp-like string instrument."),
    Proficiency(name="Horn", category="Tool", description="A brass wind instrument."),
    Proficiency(
        name="Pan Flute", category="Tool", description="A woodwind instrument with multiple pipes."
    ),
    Proficiency(name="Shawm", category="Tool", description="A predecessor to the oboe."),
    Proficiency(
        name="Viol", category="Tool", description="A bowed string instrument similar to a violin."
    ),
    # Armor
    Proficiency(
        name="Light Armor", category="Armor", description="Proficiency in wearing light armor."
    ),
    Proficiency(
        name="Medium Armor", category="Armor", description="Proficiency in wearing medium armor."
    ),
    Proficiency(
        name="Heavy Armor", category="Armor", description="Proficiency in wearing heavy armor."
    ),
    Proficiency(name="Shields", category="Armor", description="Proficiency in using shields."),
    # Weapons (Expanded List)
    Proficiency(
        name="Simple Weapons", category="Weapon", description="Proficiency in basic weapons."
    ),
    Proficiency(
        name="Martial Weapons",
        category="Weapon",
        description="Proficiency in advanced combat weapons.",
    ),
    Proficiency(name="Clubs", category="Weapon", description="A simple bludgeoning weapon."),
    Proficiency(
        name="Daggers", category="Weapon", description="A small blade, ideal for stabbing."
    ),
    Proficiency(
        name="Greatswords", category="Weapon", description="A massive sword wielded with two hands."
    ),
    Proficiency(
        name="Handaxes", category="Weapon", description="A small axe for melee or throwing."
    ),
    Proficiency(name="Javelins", category="Weapon", description="A thrown piercing weapon."),
    Proficiency(
        name="Longbows", category="Weapon", description="A ranged weapon requiring dexterity."
    ),
    Proficiency(
        name="Longswords",
        category="Weapon",
        description="A versatile sword that can be used one or two-handed.",
    ),
    Proficiency(
        name="Maces", category="Weapon", description="A bludgeoning weapon effective against armor."
    ),
    Proficiency(
        name="Quarterstaffs", category="Weapon", description="A wooden staff used as a weapon."
    ),
    Proficiency(
        name="Rapiers",
        category="Weapon",
        description="A light, finesse sword designed for thrusting.",
    ),
    Proficiency(
        name="Shortbows", category="Weapon", description="A smaller bow effective at short range."
    ),
    Proficiency(
        name="Shortswords",
        category="Weapon",
        description="A light sword used for slashing and stabbing.",
    ),
    Proficiency(
        name="Spears", category="Weapon", description="A pole weapon used for thrusting attacks."
    ),
    Proficiency(name="Warhammers", category="Weapon", description="A heavy hammer used in combat."),
    # Languages
    Proficiency(name="Common", category="Language", description="The most widely spoken language."),
    Proficiency(name="Elvish", category="Language", description="Language of the elves."),
    Proficiency(name="Dwarvish", category="Language", description="Language of the dwarves."),
    Proficiency(name="Orc", category="Language", description="Language spoken by orcs."),
    Proficiency(name="Gnomish", category="Language", description="Language of the gnomes."),
    Proficiency(
        name="Draconic", category="Language", description="Language of dragons and dragonborn."
    ),
]

session.add_all(proficiencies)
session.commit()


# --- Classes (Core 5e) ---
classes = [
    CharacterClass(
        name="Barbarian",
        description="A fierce warrior with rage-fueled might.",
        hit_die=12,
        primary_ability="Strength",
        spellcasting=False,
        saving_throws=["Strength", "Constitution"],
    ),
    CharacterClass(
        name="Bard",
        description="A performer who weaves magic through words and music.",
        hit_die=8,
        primary_ability="Charisma",
        spellcasting=True,
        saving_throws=["Dexterity", "Charisma"],
    ),
    CharacterClass(
        name="Cleric",
        description="A divine spellcaster granted power by the gods.",
        hit_die=8,
        primary_ability="Wisdom",
        spellcasting=True,
        saving_throws=["Wisdom", "Charisma"],
    ),
    CharacterClass(
        name="Druid",
        description="A priest of nature, able to transform into animals.",
        hit_die=8,
        primary_ability="Wisdom",
        spellcasting=True,
        saving_throws=["Intelligence", "Wisdom"],
    ),
    CharacterClass(
        name="Fighter",
        description="A master of weapons and armor.",
        hit_die=10,
        primary_ability="Strength or Dexterity",
        spellcasting=False,
        saving_throws=["Strength", "Constitution"],
    ),
    CharacterClass(
        name="Monk",
        description="A martial artist who harnesses ki energy.",
        hit_die=8,
        primary_ability="Dexterity and Wisdom",
        spellcasting=False,
        saving_throws=["Strength", "Dexterity"],
    ),
    CharacterClass(
        name="Paladin",
        description="A holy knight bound by sacred oaths.",
        hit_die=10,
        primary_ability="Strength and Charisma",
        spellcasting=True,
        saving_throws=["Wisdom", "Charisma"],
    ),
    CharacterClass(
        name="Ranger",
        description="A hunter and tracker of beasts and foes.",
        hit_die=10,
        primary_ability="Dexterity and Wisdom",
        spellcasting=True,
        saving_throws=["Strength", "Dexterity"],
    ),
    CharacterClass(
        name="Rogue",
        description="A stealthy character skilled in deception and precision strikes.",
        hit_die=8,
        primary_ability="Dexterity",
        spellcasting=False,
        saving_throws=["Dexterity", "Intelligence"],
    ),
    CharacterClass(
        name="Sorcerer",
        description="A spellcaster whose magic is innate.",
        hit_die=6,
        primary_ability="Charisma",
        spellcasting=True,
        saving_throws=["Constitution", "Charisma"],
    ),
    CharacterClass(
        name="Warlock",
        description="A spellcaster who gains power from a pact with a supernatural being.",
        hit_die=8,
        primary_ability="Charisma",
        spellcasting=True,
        saving_throws=["Wisdom", "Charisma"],
    ),
    CharacterClass(
        name="Wizard",
        description="A learned spellcaster who manipulates arcane energies.",
        hit_die=6,
        primary_ability="Intelligence",
        spellcasting=True,
        saving_throws=["Intelligence", "Wisdom"],
    ),
]

proficiency_dict = {p.name: p for p in session.query(Proficiency).all()}

proficiency_mapping = {
    "Barbarian": ["Light Armor", "Medium Armor", "Shields", "Simple Weapons", "Martial Weapons"],
    "Bard": [
        "Light Armor",
        "Simple Weapons",
        "Hand Crossbows",
        "Longswords",
        "Rapiers",
        "Shortswords",
    ],
    "Cleric": ["Light Armor", "Medium Armor", "Shields", "Simple Weapons"],
    "Druid": [
        "Light Armor",
        "Medium Armor",
        "Shields",
        "Clubs",
        "Daggers",
        "Quarterstaffs",
        "Scimitars",
        "Sickles",
        "Spears",
    ],
    "Fighter": ["All Armor", "Shields", "Simple Weapons", "Martial Weapons"],
    "Monk": ["Simple Weapons", "Shortswords"],
    "Paladin": ["All Armor", "Shields", "Simple Weapons", "Martial Weapons"],
    "Ranger": ["Light Armor", "Medium Armor", "Shields", "Simple Weapons", "Martial Weapons"],
    "Rogue": [
        "Light Armor",
        "Simple Weapons",
        "Hand Crossbows",
        "Longswords",
        "Rapiers",
        "Shortswords",
        "Thieves' Tools",
    ],
    "Sorcerer": ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light Crossbows"],
    "Warlock": ["Light Armor", "Simple Weapons"],
    "Wizard": ["Daggers", "Quarterstaffs", "Light Crossbows"],
}

# Assign proficiencies to classes
for character_class in classes:
    if character_class.name in proficiency_mapping:
        class_proficiencies = [
            proficiency_dict[prof_name]
            for prof_name in proficiency_mapping[character_class.name]
            if prof_name in proficiency_dict
        ]
        character_class.proficiencies = class_proficiencies

session.add_all(classes)
session.commit()
print("✅ Classes and their proficiencies successfully populated!")


# --- Backgrounds (Core 5e) ---
backgrounds = [
    Background(
        name="Acolyte",
        description="You have spent your life in the service of a temple to a specific god or"
        " pantheon.",
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
        starting_equipment=[
            "Crowbar",
            "Set of dark common clothes including a hood",
            "Belt pouch containing 15 gp",
        ],
    ),
    Background(
        name="Entertainer",
        description="You thrive in front of an audience, making the world your stage.",
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

background_proficiency_mapping = {
    "Acolyte": ["Insight", "Religion"],
    "Charlatan": ["Deception", "Sleight of Hand"],
    "Criminal": ["Deception", "Stealth"],
    "Entertainer": ["Acrobatics", "Performance"],
    "Folk Hero": ["Animal Handling", "Survival"],
    "Guild Artisan": ["Insight", "Persuasion"],
    "Hermit": ["Medicine", "Religion"],
    "Noble": ["History", "Persuasion"],
    "Outlander": ["Athletics", "Survival"],
    "Sage": ["Arcana", "History"],
    "Sailor": ["Athletics", "Perception"],
    "Soldier": ["Athletics", "Intimidation"],
    "Urchin": ["Sleight of Hand", "Stealth"],
}

# Assign proficiencies to backgrounds
for background in backgrounds:
    if background.name in background_proficiency_mapping:
        background_proficiencies = [
            proficiency_dict[prof_name]
            for prof_name in background_proficiency_mapping[background.name]
            if prof_name in proficiency_dict
        ]
        background.starting_proficiencies = background_proficiencies


# --- Insert Data into Database ---
session.add_all(backgrounds)
session.commit()
print("✅ Backgrounds and their proficiencies successfully populated!")

# Close the session
session.close()
