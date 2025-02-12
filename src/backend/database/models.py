"""Defines models for game database."""

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import declarative_base, relationship

from src.utils import weighted_random_stat

Base = declarative_base()


# Traits table
class Trait(Base):
    """Defines character traits that races can have."""

    __tablename__ = "traits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    index = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    proficiencies = Column(JSON, nullable=True)


# Proficiencies table
class Proficiency(Base):
    """Defines proficiencies including skills, tools, weapons, and languages."""

    __tablename__ = "proficiencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)  # Skill, Tool, Weapon, Language
    description = Column(Text)

    def __repr__(self):
        return f"<Proficiency(name={self.name}, category={self.category})>"


class Equipment(Base):
    """Defines equipment items available in D&D 5e."""

    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)  # e.g., "Weapon", "Armor", "Adventuring Gear"
    cost = Column(Float, nullable=False)  # Cost in gold pieces
    weight = Column(Float, nullable=True)  # Weight in pounds
    description = Column(Text, nullable=True)

    # Weapon-specific attributes
    damage = Column(String, nullable=True)  # E.g., "1d8 slashing"
    properties = Column(JSON, nullable=True)  # E.g., ["Light", "Finesse"]

    # Armor-specific attributes
    armor_class = Column(Integer, nullable=True)
    stealth_disadvantage = Column(Boolean, default=False)
    strength_requirement = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Equipment(name={self.name}, category={self.category})>"


# Junction tables for race/class/background to trait/proficinecies/equipment mappings
RaceTrait = Table(
    "race_traits",
    Base.metadata,
    Column("race_id", Integer, ForeignKey("races.id"), primary_key=True),
    Column("trait_id", Integer, ForeignKey("traits.id"), primary_key=True),
)


ClassProficiencies = Table(
    "class_proficiencies",
    Base.metadata,
    Column("class_id", Integer, ForeignKey("classes.id"), primary_key=True),
    Column("proficiency_id", Integer, ForeignKey("proficiencies.id"), primary_key=True),
)

BackgroundProficiencies = Table(
    "background_proficiencies",
    Base.metadata,
    Column("background_id", Integer, ForeignKey("backgrounds.id"), primary_key=True),
    Column("proficiency_id", Integer, ForeignKey("proficiencies.id"), primary_key=True),
)

BackgroundEquipment = Table(
    "background_equipment",
    Base.metadata,
    Column("background_id", Integer, ForeignKey("backgrounds.id"), primary_key=True),
    Column("equipment_id", Integer, ForeignKey("equipment.id"), primary_key=True),
)

ClassEquipment = Table(
    "class_equipment",
    Base.metadata,
    Column("class_id", Integer, ForeignKey("classes.id"), primary_key=True),
    Column("equipment_id", Integer, ForeignKey("equipment.id"), primary_key=True),
)

# Junction table for mapping Character to current inventoty
CharacterInventory = Table(
    "character_inventory",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id"), primary_key=True),
    Column("equipment_id", Integer, ForeignKey("equipment.id"), primary_key=True),
)


# Races Table
class Race(Base):
    """Defines available races in D&D with default stat bonuses."""

    __tablename__ = "races"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    strength_bonus = Column(Integer, default=0)
    dexterity_bonus = Column(Integer, default=0)
    constitution_bonus = Column(Integer, default=0)
    intelligence_bonus = Column(Integer, default=0)
    wisdom_bonus = Column(Integer, default=0)
    charisma_bonus = Column(Integer, default=0)
    speed = Column(Integer, default=30)
    traits = relationship("Trait", secondary=RaceTrait, backref="races")

    def __repr__(self):
        return f"<Race(name={self.name})>"


# Classes Table
class CharacterClass(Base):
    """Defines available character classes."""

    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    hit_die = Column(Integer)
    primary_ability = Column(String)
    proficiencies = relationship("Proficiency", secondary=ClassProficiencies, backref="classes")
    spellcasting = Column(Boolean, default=False)
    saving_throws = Column(JSON, nullable=False)
    starting_equipment = relationship(
        "Equipment",
        secondary=ClassEquipment,
        backref="classes",
    )

    def __repr__(self):
        return f"<Class(name={self.name})>"


# Backgrounds Table
class Background(Base):
    """Defines D&D backgrounds that influence character skills & equipment."""

    __tablename__ = "backgrounds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    starting_gold = Column(Float)
    starting_proficiencies = relationship(
        "Proficiency", secondary=BackgroundProficiencies, backref="backgrounds"
    )
    starting_equipment = relationship(
        "Equipment",
        secondary=BackgroundEquipment,
        backref="backgrounds",
    )

    def __repr__(self):
        return f"<Background(name={self.name})>"


# Characters Table
class Character(Base):
    """Defines player-created characters.

    Leverages deafults to complete character sheets when user input is incomplete
    """

    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    race_id = Column(Integer, ForeignKey("races.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    background_id = Column(Integer, ForeignKey("backgrounds.id"))

    current_hit_points = Column(Integer)
    gold = Column(Float, default=0.0)

    strength = Column(Integer, default=weighted_random_stat)
    dexterity = Column(Integer, default=weighted_random_stat)
    constitution = Column(Integer, default=weighted_random_stat)
    intelligence = Column(Integer, default=weighted_random_stat)
    wisdom = Column(Integer, default=weighted_random_stat)
    charisma = Column(Integer, default=weighted_random_stat)

    race = relationship("Race")
    char_class = relationship("CharacterClass")
    background = relationship("Background")

    inventory = relationship(
        "Equipment",
        secondary=CharacterInventory,
        backref="characters",
    )

    def __repr__(self):
        return f"<Character(name={self.name}, class={self.char_class.name}, race={self.race.name})>"
