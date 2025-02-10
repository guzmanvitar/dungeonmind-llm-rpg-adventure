"""Defines models for game database."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import declarative_base, relationship

from src.utils import weighted_random_stat

Base = declarative_base()


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
    abilities = Column(JSON)  # List of racial abilities (e.g., ["Darkvision", "Fey Ancestry"])

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
    primary_ability = Column(String)  # E.g., "Strength" for Barbarian
    proficiencies = Column(JSON)  # List of skills/weapons/spells
    spellcasting = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Class(name={self.name})>"


# Backgrounds Table
class Background(Base):
    """Defines D&D backgrounds that influence character skills & equipment."""

    __tablename__ = "backgrounds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    starting_proficiencies = Column(JSON)  # List of proficiencies gained
    starting_equipment = Column(JSON)  # List of starting equipment

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

    strength = Column(Integer, default=weighted_random_stat)
    dexterity = Column(Integer, default=weighted_random_stat)
    constitution = Column(Integer, default=weighted_random_stat)
    intelligence = Column(Integer, default=weighted_random_stat)
    wisdom = Column(Integer, default=weighted_random_stat)
    charisma = Column(Integer, default=weighted_random_stat)

    race = relationship("Race")
    char_class = relationship("CharacterClass")
    background = relationship("Background")

    def __repr__(self):
        return f"<Character(name={self.name}, class={self.char_class.name}, race={self.race.name})>"


# Abilities Table
class Ability(Base):
    """Defines special abilities like Darkvision, Sneak Attack, etc."""

    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)

    def __repr__(self):
        return f"<Ability(name={self.name})>"


# Character Abilities Linking Table
class CharacterAbility(Base):
    """Links characters with their acquired abilities."""

    __tablename__ = "character_abilities"

    character_id = Column(Integer, ForeignKey("characters.id"), primary_key=True)
    ability_id = Column(Integer, ForeignKey("abilities.id"), primary_key=True)


# Skills Table
class Skill(Base):
    """Defines skills (Stealth, Persuasion, Athletics)."""

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    related_stat = Column(String)  # Strength, Dexterity, etc.
    description = Column(Text)

    def __repr__(self):
        return f"<Skill(name={self.name})>"


# Character Skills Linking Table
class CharacterSkill(Base):
    """Links characters to their skill proficiencies."""

    __tablename__ = "character_skills"

    character_id = Column(Integer, ForeignKey("characters.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)
