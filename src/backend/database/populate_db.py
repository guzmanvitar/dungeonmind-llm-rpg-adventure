"""Populates game db with core game entities"""

from sqlalchemy.orm import Session

from src.backend.database.config import engine
from src.backend.database.models import (
    Background,
    CharacterClass,
    Equipment,
    Proficiency,
    Race,
    Trait,
)

# -- Raw Data ---
# Traits
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


# Races
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

# Proficiencies (categorized by type)
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

# Equipments (categorized by type)
equipment_items = [
    # Simple Melee Weapons
    Equipment(
        name="Club",
        category="Weapon",
        cost=0.1,
        weight=2,
        description="A simple wooden club.",
        damage="1d4 bludgeoning",
        properties=["Light"],
    ),
    Equipment(
        name="Dagger",
        category="Weapon",
        cost=2,
        weight=1,
        description="A small, sharp blade.",
        damage="1d4 piercing",
        properties=["Finesse", "Light", "Thrown (range 20/60)"],
    ),
    Equipment(
        name="Greatclub",
        category="Weapon",
        cost=0.2,
        weight=10,
        description="A large, heavy club.",
        damage="1d8 bludgeoning",
        properties=["Two-Handed"],
    ),
    Equipment(
        name="Handaxe",
        category="Weapon",
        cost=5,
        weight=2,
        description="A small axe suitable for throwing.",
        damage="1d6 slashing",
        properties=["Light", "Thrown (range 20/60)"],
    ),
    Equipment(
        name="Javelin",
        category="Weapon",
        cost=0.5,
        weight=2,
        description="A light spear designed for throwing.",
        damage="1d6 piercing",
        properties=["Thrown (range 30/120)"],
    ),
    Equipment(
        name="Light Hammer",
        category="Weapon",
        cost=2,
        weight=2,
        description="A small hammer suitable for throwing.",
        damage="1d4 bludgeoning",
        properties=["Light", "Thrown (range 20/60)"],
    ),
    Equipment(
        name="Mace",
        category="Weapon",
        cost=5,
        weight=4,
        description="A heavy club with a metal head.",
        damage="1d6 bludgeoning",
        properties=[],
    ),
    Equipment(
        name="Quarterstaff",
        category="Weapon",
        cost=0.2,
        weight=4,
        description="A sturdy wooden staff.",
        damage="1d6 bludgeoning",
        properties=["Versatile (1d8)"],
    ),
    Equipment(
        name="Sickle",
        category="Weapon",
        cost=1,
        weight=2,
        description="A curved blade used for harvesting.",
        damage="1d4 slashing",
        properties=["Light"],
    ),
    Equipment(
        name="Spear",
        category="Weapon",
        cost=1,
        weight=3,
        description="A long shaft with a pointed tip.",
        damage="1d6 piercing",
        properties=["Thrown (range 20/60)", "Versatile (1d8)"],
    ),
    # Simple Ranged Weapons
    Equipment(
        name="Light Crossbow",
        category="Weapon",
        cost=25,
        weight=5,
        description="A small crossbow.",
        damage="1d8 piercing",
        properties=["Ammunition (range 80/320)", "Loading", "Two-Handed"],
    ),
    Equipment(
        name="Dart",
        category="Weapon",
        cost=0.05,
        weight=0.25,
        description="A small, pointed throwing weapon.",
        damage="1d4 piercing",
        properties=["Finesse", "Thrown (range 20/60)"],
    ),
    Equipment(
        name="Shortbow",
        category="Weapon",
        cost=25,
        weight=2,
        description="A short wooden bow.",
        damage="1d6 piercing",
        properties=["Ammunition (range 80/320)", "Two-Handed"],
    ),
    Equipment(
        name="Sling",
        category="Weapon",
        cost=0.1,
        weight=0,
        description="A simple leather sling.",
        damage="1d4 bludgeoning",
        properties=["Ammunition (range 30/120)"],
    ),
    # Martial Melee Weapons
    Equipment(
        name="Battleaxe",
        category="Weapon",
        cost=10,
        weight=4,
        description="A versatile axe used in combat.",
        damage="1d8 slashing",
        properties=["Versatile"],
    ),
    Equipment(
        name="Flail",
        category="Weapon",
        cost=10,
        weight=2,
        description="A spiked metal ball attached to a chain.",
        damage="1d8 bludgeoning",
        properties=[],
    ),
    Equipment(
        name="Glaive",
        category="Weapon",
        cost=20,
        weight=6,
        description="A polearm with a large curved blade.",
        damage="1d10 slashing",
        properties=["Heavy", "Reach", "Two-Handed"],
    ),
    Equipment(
        name="Greataxe",
        category="Weapon",
        cost=30,
        weight=7,
        description="A massive axe wielded with both hands.",
        damage="1d12 slashing",
        properties=["Heavy", "Two-Handed"],
    ),
    Equipment(
        name="Greatsword",
        category="Weapon",
        cost=50,
        weight=6,
        description="A huge sword requiring two hands.",
        damage="2d6 slashing",
        properties=["Heavy", "Two-Handed"],
    ),
    Equipment(
        name="Halberd",
        category="Weapon",
        cost=20,
        weight=6,
        description="A polearm with an axe blade and spear point.",
        damage="1d10 slashing",
        properties=["Heavy", "Reach", "Two-Handed"],
    ),
    Equipment(
        name="Lance",
        category="Weapon",
        cost=10,
        weight=6,
        description="A long spear used while mounted.",
        damage="1d12 piercing",
        properties=["Reach", "Special"],
    ),
    Equipment(
        name="Longsword",
        category="Weapon",
        cost=15,
        weight=3,
        description="A balanced sword for versatile use.",
        damage="1d8 slashing",
        properties=["Versatile"],
    ),
    Equipment(
        name="Maul",
        category="Weapon",
        cost=10,
        weight=10,
        description="A two-handed hammer with great impact.",
        damage="2d6 bludgeoning",
        properties=["Heavy", "Two-Handed"],
    ),
    Equipment(
        name="Morningstar",
        category="Weapon",
        cost=15,
        weight=4,
        description="A club-like weapon with spikes.",
        damage="1d8 piercing",
        properties=[],
    ),
    Equipment(
        name="Pike",
        category="Weapon",
        cost=5,
        weight=18,
        description="A long spear used for thrusting attacks.",
        damage="1d10 piercing",
        properties=["Heavy", "Reach", "Two-Handed"],
    ),
    Equipment(
        name="Rapier",
        category="Weapon",
        cost=25,
        weight=2,
        description="A thin, agile sword used for piercing attacks.",
        damage="1d8 piercing",
        properties=["Finesse"],
    ),
    Equipment(
        name="Scimitar",
        category="Weapon",
        cost=25,
        weight=3,
        description="A curved sword good for slashing attacks.",
        damage="1d6 slashing",
        properties=["Finesse", "Light"],
    ),
    Equipment(
        name="Shortsword",
        category="Weapon",
        cost=10,
        weight=2,
        description="A small, agile sword.",
        damage="1d6 piercing",
        properties=["Finesse", "Light"],
    ),
    Equipment(
        name="Trident",
        category="Weapon",
        cost=5,
        weight=4,
        description="A three-pronged spear.",
        damage="1d6 piercing",
        properties=["Thrown", "Versatile"],
    ),
    Equipment(
        name="Warhammer",
        category="Weapon",
        cost=15,
        weight=2,
        description="A heavy hammer used for crushing attacks.",
        damage="1d8 bludgeoning",
        properties=["Versatile"],
    ),
    Equipment(
        name="Whip",
        category="Weapon",
        cost=2,
        weight=3,
        description="A flexible weapon used for entangling opponents.",
        damage="1d4 slashing",
        properties=["Finesse", "Reach"],
    ),
    # Martial Ranged Weapons
    Equipment(
        name="Blowgun",
        category="Weapon",
        cost=10,
        weight=1,
        description="A small tube used for firing darts.",
        damage="1 piercing",
        properties=["Ammunition", "Loading"],
    ),
    Equipment(
        name="Hand Crossbow",
        category="Weapon",
        cost=75,
        weight=3,
        description="A small crossbow for one-handed use.",
        damage="1d6 piercing",
        properties=["Ammunition", "Light", "Loading"],
    ),
    Equipment(
        name="Heavy Crossbow",
        category="Weapon",
        cost=50,
        weight=18,
        description="A powerful, slow-loading crossbow.",
        damage="1d10 piercing",
        properties=["Ammunition", "Heavy", "Loading", "Two-Handed"],
    ),
    Equipment(
        name="Longbow",
        category="Weapon",
        cost=50,
        weight=2,
        description="A large, powerful bow.",
        damage="1d8 piercing",
        properties=["Ammunition", "Heavy", "Two-Handed"],
    ),
    Equipment(
        name="Net",
        category="Weapon",
        cost=1,
        weight=3,
        description="A thrown net used for entangling creatures.",
        damage="None",
        properties=["Special", "Thrown"],
    ),
    # Heavy Armor
    Equipment(
        name="Ring Mail",
        category="Armor",
        cost=30,
        weight=40,
        description="A suit of armor with interlocking metal rings.",
        armor_class=14,
        stealth_disadvantage=True,
        strength_requirement=None,
    ),
    Equipment(
        name="Chain Mail",
        category="Armor",
        cost=75,
        weight=55,
        description="Armor made of interlocking metal rings.",
        armor_class=16,
        stealth_disadvantage=True,
        strength_requirement=13,
    ),
    Equipment(
        name="Splint",
        category="Armor",
        cost=200,
        weight=60,
        description="Armor reinforced with metal strips.",
        armor_class=17,
        stealth_disadvantage=True,
        strength_requirement=15,
    ),
    Equipment(
        name="Plate",
        category="Armor",
        cost=1500,
        weight=65,
        description="Full metal armor that offers maximum protection.",
        armor_class=18,
        stealth_disadvantage=True,
        strength_requirement=15,
    ),
    # Medium Armor
    Equipment(
        name="Hide Armor",
        category="Armor",
        cost=10,
        weight=12,
        description="Armor made from thick furs and animal hides.",
        armor_class=12,
        stealth_disadvantage=False,
        strength_requirement=None,
    ),
    Equipment(
        name="Chain Shirt",
        category="Armor",
        cost=50,
        weight=20,
        description="A shirt of interlocking metal rings worn under clothing.",
        armor_class=13,
        stealth_disadvantage=False,
        strength_requirement=None,
    ),
    Equipment(
        name="Scale Mail",
        category="Armor",
        cost=50,
        weight=45,
        description="Metal scales sewn onto leather armor.",
        armor_class=14,
        stealth_disadvantage=True,
        strength_requirement=None,
    ),
    Equipment(
        name="Breastplate",
        category="Armor",
        cost=400,
        weight=20,
        description="A fitted metal chestplate worn over normal clothing.",
        armor_class=14,
        stealth_disadvantage=False,
        strength_requirement=None,
    ),
    Equipment(
        name="Half Plate",
        category="Armor",
        cost=750,
        weight=40,
        description="Metal plates covering most of the body.",
        armor_class=15,
        stealth_disadvantage=True,
        strength_requirement=None,
    ),
    # Light Armor
    Equipment(
        name="Padded Armor",
        category="Armor",
        cost=5,
        weight=8,
        description="A quilted, padded garment that offers basic protection.",
        armor_class=11,
        stealth_disadvantage=True,
        strength_requirement=None,
    ),
    Equipment(
        name="Leather Armor",
        category="Armor",
        cost=10,
        weight=10,
        description="Tough but flexible leather armor.",
        armor_class=11,
        stealth_disadvantage=False,
        strength_requirement=None,
    ),
    Equipment(
        name="Studded Leather Armor",
        category="Armor",
        cost=45,
        weight=13,
        description="Leather armor reinforced with metal studs.",
        armor_class=12,
        stealth_disadvantage=False,
        strength_requirement=None,
    ),
    # Shields
    Equipment(
        name="Shield",
        category="Armor",
        cost=10,
        weight=6,
        description="A shield that grants additional defense.",
        armor_class=2,
        stealth_disadvantage=False,
        strength_requirement=None,
    ),
    # Adventuring Gear
    Equipment(
        name="Abacus",
        category="Adventuring Gear",
        cost=2,
        weight=2,
        description="A simple counting tool.",
    ),
    Equipment(
        name="Backpack",
        category="Adventuring Gear",
        cost=2,
        weight=5,
        description="A sturdy pack for carrying gear.",
    ),
    Equipment(
        name="Ball Bearings (1,000)",
        category="Adventuring Gear",
        cost=1,
        weight=2,
        description="A pouch of tiny metal spheres used to trip foes.",
    ),
    Equipment(
        name="Bedroll",
        category="Adventuring Gear",
        cost=1,
        weight=7,
        description="A thick blanket for sleeping.",
    ),
    Equipment(
        name="Bell",
        category="Adventuring Gear",
        cost=1,
        weight=0,
        description="A small metal bell.",
    ),
    Equipment(
        name="Candle",
        category="Adventuring Gear",
        cost=0.01,
        weight=0,
        description="A wax candle for light.",
    ),
    Equipment(
        name="Chain (10 feet)",
        category="Adventuring Gear",
        cost=5,
        weight=10,
        description="A length of iron chain.",
    ),
    Equipment(
        name="Chalk (1 piece)",
        category="Adventuring Gear",
        cost=0.01,
        weight=0,
        description="A piece of chalk for writing.",
    ),
    Equipment(
        name="Chest",
        category="Adventuring Gear",
        cost=5,
        weight=25,
        description="A wooden chest for storing valuables.",
    ),
    Equipment(
        name="Crowbar",
        category="Adventuring Gear",
        cost=2,
        weight=5,
        description="A metal pry bar.",
    ),
    Equipment(
        name="Fishing Tackle",
        category="Adventuring Gear",
        cost=1,
        weight=4,
        description="A kit for fishing.",
    ),
    Equipment(
        name="Flask or Tankard",
        category="Adventuring Gear",
        cost=0.02,
        weight=1,
        description="A container for holding liquid.",
    ),
    Equipment(
        name="Grappling Hook",
        category="Adventuring Gear",
        cost=2,
        weight=4,
        description="A hook used for climbing.",
    ),
    Equipment(
        name="Hammer",
        category="Adventuring Gear",
        cost=1,
        weight=3,
        description="A simple tool for driving nails.",
    ),
    Equipment(
        name="Healer’s Kit",
        category="Adventuring Gear",
        cost=5,
        weight=3,
        description="A kit containing bandages and medicines.",
    ),
    Equipment(
        name="Hooded Lantern",
        category="Adventuring Gear",
        cost=5,
        weight=2,
        description="A lantern with a hood to control light.",
    ),
    Equipment(
        name="Ink and Quill",
        category="Adventuring Gear",
        cost=10,
        weight=0,
        description="A quill and a bottle of ink for writing.",
    ),
    Equipment(
        name="Ink Pen",
        category="Adventuring Gear",
        cost=0.02,
        weight=0,
        description="A simple pen for writing.",
    ),
    Equipment(
        name="Ladder (10 feet)",
        category="Adventuring Gear",
        cost=1,
        weight=25,
        description="A wooden ladder.",
    ),
    Equipment(
        name="Lamp",
        category="Adventuring Gear",
        cost=0.5,
        weight=1,
        description="A simple oil-burning lamp.",
    ),
    Equipment(
        name="Lock",
        category="Adventuring Gear",
        cost=10,
        weight=1,
        description="A small metal lock with a key.",
    ),
    Equipment(
        name="Magnifying Glass",
        category="Adventuring Gear",
        cost=100,
        weight=0,
        description="A glass lens used to magnify objects.",
    ),
    Equipment(
        name="Manacles",
        category="Adventuring Gear",
        cost=2,
        weight=6,
        description="Metal restraints for prisoners.",
    ),
    Equipment(
        name="Mess Kit",
        category="Adventuring Gear",
        cost=0.2,
        weight=1,
        description="A set of eating utensils.",
    ),
    Equipment(
        name="Mirror, Steel",
        category="Adventuring Gear",
        cost=5,
        weight=0.5,
        description="A small steel mirror.",
    ),
    Equipment(
        name="Oil (1 flask)",
        category="Adventuring Gear",
        cost=0.1,
        weight=1,
        description="A flask of oil for burning.",
    ),
    Equipment(
        name="Potion of Healing",
        category="Adventuring Gear",
        cost=50,
        weight=0.5,
        description="A magical potion that restores health.",
    ),
    Equipment(
        name="Rations (1 day)",
        category="Adventuring Gear",
        cost=0.5,
        weight=2,
        description="Preserved food for travel.",
    ),
    Equipment(
        name="Rope (50 feet, hempen)",
        category="Adventuring Gear",
        cost=1,
        weight=10,
        description="A strong rope for climbing.",
    ),
    Equipment(
        name="Sack",
        category="Adventuring Gear",
        cost=0.01,
        weight=0.5,
        description="A simple cloth bag.",
    ),
    Equipment(
        name="Shovel",
        category="Adventuring Gear",
        cost=2,
        weight=5,
        description="A tool for digging.",
    ),
    Equipment(
        name="Signal Whistle",
        category="Adventuring Gear",
        cost=0.05,
        weight=0,
        description="A small whistle for signaling.",
    ),
    Equipment(
        name="Spyglass",
        category="Adventuring Gear",
        cost=1000,
        weight=1,
        description="A telescope for long-distance viewing.",
    ),
    Equipment(
        name="Tent (two-person)",
        category="Adventuring Gear",
        cost=2,
        weight=20,
        description="A portable shelter for two people.",
    ),
    Equipment(
        name="Tinderbox",
        category="Adventuring Gear",
        cost=0.5,
        weight=1,
        description="A box containing flint and steel for making fire.",
    ),
    Equipment(
        name="Torch",
        category="Adventuring Gear",
        cost=0.01,
        weight=1,
        description="A wooden torch for illumination.",
    ),
    Equipment(
        name="Waterskin",
        category="Adventuring Gear",
        cost=0.2,
        weight=5,
        description="A leather container for holding water.",
    ),
    Equipment(
        name="Whetstone",
        category="Adventuring Gear",
        cost=0.01,
        weight=1,
        description="A stone used for sharpening weapons.",
    ),
    Equipment(
        name="Lute",
        category="Adventuring Gear",
        cost=35.0,
        weight=2.0,
        description="A stringed musical instrument commonly used by bards for performances.",
    ),
    Equipment(
        name="Druidic Focus",
        category="Adventuring Gear",
        cost=5.0,
        weight=1.0,
        description="A natural object (mistletoe, totem, staff, etc.) that serves as a spellcasting"
        " focus for Druids.",
    ),
    Equipment(
        name="Thieves' Tools",
        category="Adventuring Gear",
        cost=25.0,
        weight=1.0,
        description="A set of tools including lock picks and small gadgets, used for disabling"
        " traps and picking locks.",
    ),
    Equipment(
        name="Arcane Focus",
        category="Adventuring Gear",
        cost=10.0,
        weight=1.0,
        description="A crystal, orb, rod, staff, or wand that functions as a spellcasting focus for"
        " Sorcerers, Warlocks, and Wizards.",
    ),
    Equipment(
        name="Spellbook",
        category="Adventuring Gear",
        cost=50.0,
        weight=3.0,
        description="A book containing a Wizard's spells, written in magical script.",
    ),
    Equipment(
        name="Holy Symbol",
        category="Adventuring Gear",
        cost=5.0,
        weight=1.0,
        description="A symbol of a deity used by Clerics and Paladins as a spellcasting focus.",
    ),
    Equipment(
        name="Costume",
        category="Adventuring Gear",
        cost=5.0,
        weight=4.0,
        description="A set of clothes used for performances or disguises.",
    ),
    Equipment(
        name="Signet Ring",
        category="Adventuring Gear",
        cost=5.0,
        weight=0.1,
        description="A ring bearing a family crest or insignia, symbolizing noble status.",
    ),
    Equipment(
        name="Hunting Trap",
        category="Adventuring Gear",
        cost=5.0,
        weight=25.0,
        description="A large trap used to capture beasts, commonly carried by outlanders.",
    ),
    Equipment(
        name="Deck of Cards",
        category="Adventuring Gear",
        cost=1.0,
        weight=0.5,
        description="A standard deck of playing cards, sometimes used for gambling.",
    ),
    Equipment(
        name="Set of Bone Dice",
        category="Adventuring Gear",
        cost=1.0,
        weight=0.5,
        description="A set of carved bone dice used for games of chance.",
    ),
    Equipment(
        name="Fine Clothes",
        category="Adventuring Gear",
        cost=15.0,
        weight=6.0,
        description="A set of high-quality garments suited for noble or formal occasions.",
    ),
    Equipment(
        name="Disguise Kit",
        category="Adventuring Gear",
        cost=25.0,
        weight=3.0,
        description="A small box containing makeup, hair dye, and small props for disguises.",
    ),
    Equipment(
        name="Common Clothes",
        category="Adventuring Gear",
        cost=5.0,
        weight=3.0,
        description="A set of basic, everyday clothing.",
    ),
    Equipment(
        name="Set of Artisan's Tools",
        category="Adventuring Gear",
        cost=10.0,
        weight=5.0,
        description="A set of tools used by artisans for crafting and repairing goods.",
    ),
    Equipment(
        name="Letter of Introduction",
        category="Adventuring Gear",
        cost=0.0,
        weight=0.1,
        description="A letter bearing the seal of a guild or noble, granting access to certain"
        " privileges.",
    ),
    Equipment(
        name="Herbalism Kit",
        category="Adventuring Gear",
        cost=5.0,
        weight=3.0,
        description="A small collection of tools used to create herbal remedies and potions.",
    ),
    Equipment(
        name="Scroll of Pedigree",
        category="Adventuring Gear",
        cost=0.0,
        weight=0.1,
        description="A document proving a noble's lineage and family history.",
    ),
    Equipment(
        name="Silk Rope",
        category="Adventuring Gear",
        cost=10.0,
        weight=5.0,
        description="A 50-foot length of silk rope, lighter and stronger than hemp rope.",
    ),
    Equipment(
        name="Lucky Charm",
        category="Adventuring Gear",
        cost=0.0,
        weight=0.1,
        description="A small trinket believed to bring good luck.",
    ),
    Equipment(
        name="Insignia of Rank",
        category="Adventuring Gear",
        cost=5.0,
        weight=0.5,
        description="A badge or symbol denoting military or noble status.",
    ),
    Equipment(
        name="City Map",
        category="Adventuring Gear",
        cost=5.0,
        weight=0.2,
        description="A map detailing the streets, buildings, and notable locations of a city.",
    ),
]

# Classes
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

# Backgrounds
backgrounds = [
    Background(
        name="Acolyte",
        starting_gold=10.0,
        description="You have spent your life in the service of a temple to a specific god or"
        " pantheon.",
    ),
    Background(
        name="Charlatan",
        starting_gold=15.0,
        description="You have always had a way with people, and you know how to make them trust "
        "you.",
    ),
    Background(
        name="Criminal",
        starting_gold=15.0,
        description="You are an experienced criminal with a history of breaking the law.",
    ),
    Background(
        name="Entertainer",
        starting_gold=10.0,
        description="You thrive in front of an audience, making the world your stage.",
    ),
    Background(
        name="Folk Hero",
        starting_gold=10.0,
        description="You come from a humble social rank, but you are destined for so much more.",
    ),
    Background(
        name="Guild Artisan",
        starting_gold=15.0,
        description="You are a member of an artisan's guild, skilled in a particular field and"
        " closely associated with other artisans.",
    ),
    Background(
        name="Hermit",
        starting_gold=5.0,
        description="You lived in seclusion, either in a sheltered community or entirely alone.",
    ),
    Background(
        name="Noble",
        starting_gold=25.0,
        description="You understand wealth, power, and privilege.",
    ),
    Background(
        name="Outlander",
        starting_gold=10.0,
        description="You grew up in the wilds, far from civilization and the comforts of town and"
        " technology.",
    ),
    Background(
        name="Sage",
        starting_gold=5.0,
        description="You spent years learning the lore of the multiverse.",
    ),
    Background(
        name="Sailor",
        starting_gold=15.0,
        description="You sailed on a seagoing vessel for years.",
    ),
    Background(
        name="Soldier",
        starting_gold=10.0,
        description="You are a battle-tested warrior.",
    ),
    Background(
        name="Urchin",
        starting_gold=3.0,
        description="You grew up on the streets alone, orphaned, and poor.",
    ),
]


# --- Mappings ---
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


starting_equipment_mapping = {
    "Barbarian": ["Greataxe", "Handaxe"],
    "Bard": ["Rapier", "Leather Armor", "Lute"],
    "Cleric": ["Mace", "Scale Mail", "Shield"],
    "Druid": ["Quarterstaff", "Leather Armor", "Druidic Focus"],
    "Fighter": ["Longsword", "Handaxe", "Chain Mail", "Shield", "Light Crossbow"],
    "Monk": ["Shortsword", "Dart"],
    "Paladin": ["Greatsword", "Chain Mail", "Shield"],
    "Ranger": ["Longbow", "Leather Armor", "Shortsword"],
    "Rogue": ["Rapier", "Leather Armor", "Dagger", "Thieves' Tools"],
    "Sorcerer": ["Quarterstaff", "Arcane Focus"],
    "Warlock": ["Dagger", "Leather Armor", "Arcane Focus"],
    "Wizard": ["Quarterstaff", "Spellbook"],
}

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


background_equipment_mapping = {
    "Acolyte": ["Holy Symbol"],
    "Charlatan": ["Fine Clothes", "Disguise Kit", "Deck of Cards"],
    "Criminal": ["Crowbar", "Common Clothes"],
    "Entertainer": ["Lute", "Costume"],
    "Folk Hero": ["Set of Artisan's Tools", "Shovel"],
    "Guild Artisan": ["Set of Artisan's Tools", "Letter of Introduction"],
    "Hermit": ["Herbalism Kit"],
    "Noble": ["Fine Clothes", "Signet Ring", "Scroll of Pedigree"],
    "Outlander": ["Hunting Trap"],
    "Sage": [
        "Ink and Quill",
    ],
    "Sailor": ["Silk Rope", "Lucky Charm"],
    "Soldier": ["Insignia of Rank", "Set of Bone Dice"],
    "Urchin": ["City Map"],
}


def bulk_insert(session: Session):
    """Inserts listed data into session defined database"""
    session.add_all(traits)
    session.commit()

    trait_map = {trait.index: trait for trait in session.query(Trait).all()}

    for race in races:
        if race.name in race_traits:
            for trait_index in race_traits[race.name]:
                if trait_index in trait_map:
                    race.traits.append(trait_map[trait_index])

    session.add_all(races)
    session.commit()

    print("✅ Races successfully populated along with their Trait mappings!")

    session.add_all(proficiencies)
    session.commit()

    proficiency_dict = {p.name: p for p in session.query(Proficiency).all()}

    # Assign proficiencies to classes
    for character_class in classes:
        if character_class.name in proficiency_mapping:
            class_proficiencies = [
                proficiency_dict[prof_name]
                for prof_name in proficiency_mapping[character_class.name]
                if prof_name in proficiency_dict
            ]
            character_class.proficiencies = class_proficiencies

    session.add_all(equipment_items)
    session.commit()

    equipment_dict = {e.name: e for e in session.query(Equipment).all()}

    # Assign starting equipment to classes
    for character_class in classes:
        if character_class.name in starting_equipment_mapping:
            class_equipment = [
                equipment_dict[item_name]
                for item_name in starting_equipment_mapping[character_class.name]
                if item_name in equipment_dict
            ]
            character_class.starting_equipment = class_equipment  # Assign equipment

    session.add_all(classes)
    session.commit()
    print(
        "✅ Classes successfully populated along with their proficiencies and starting equipments!"
    )

    # Assign proficiencies to backgrounds
    for background in backgrounds:
        if background.name in background_proficiency_mapping:
            background_proficiencies = [
                proficiency_dict[prof_name]
                for prof_name in background_proficiency_mapping[background.name]
                if prof_name in proficiency_dict
            ]
            background.starting_proficiencies = background_proficiencies

    # Assign starting equipment to backgrounds
    for background in backgrounds:
        if background.name in background_equipment_mapping:
            background_equipment = [
                equipment_dict[item_name]
                for item_name in background_equipment_mapping[background.name]
                if item_name in equipment_dict
            ]
            background.starting_equipment = background_equipment

    session.add_all(backgrounds)
    session.commit()
    print(
        "✅ Backgrounds successfully populated along with their proficiencies and starting"
        " equipments"
    )

    # Close the session
    session.close()


if __name__ == "__main__":
    # Create a new database session
    local_session = Session(bind=engine)

    # Insert Data into Database
    bulk_insert(local_session)
