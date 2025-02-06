"""
FastAPI orchestrator for the DungeonMind project.

This module provides an API for handling chat interactions with a language model (LLM).
It processes user input, maintains conversation history, and generates AI-driven responses.
"""

import json

import yaml
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.backend.database.config import SessionLocal
from src.backend.database.models import Background, Character, CharacterClass, Race
from src.backend.orchestrator.models import ChatRequest, ChatResponse
from src.backend.orchestrator.routes.character import router as character_router
from src.backend.orchestrator.services import LLMService, ModelFactory
from src.constants import BACKEND_CONFIG
from src.logger_definition import get_logger

logger = get_logger(__file__)


# Initialize FastAPI app
app = FastAPI(docs_url="/")

# Include character endpoint
app.include_router(character_router, tags=["character"])

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_llm_service() -> LLMService | None:
    """Dependency injection for selecting the LLM service."""
    # Initialize ModelFactory with selected backend
    with open(BACKEND_CONFIG, encoding="utf-8") as file:
        selected_backend = yaml.safe_load(file).get("selected_backend", "samplev1")

    model_factory = ModelFactory(selected_backend)
    llm_service = model_factory.get_model_service()

    return llm_service


def get_db():
    """Dependency to get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_available_options(
    db: Session,
) -> tuple[list[str], list[str], list[str]]:
    """Fetch all available races, classes, and backgrounds from the database."""
    races = [race.name for race in db.query(Race).all()]
    classes = [char_class.name for char_class in db.query(CharacterClass).all()]
    backgrounds = [background.name for background in db.query(Background).all()]
    return races, classes, backgrounds


def parse_character_from_text(llm_service: LLMService, user_message: str, db: Session):
    """
    Uses the new one-off LLM call to extract race, class, and background from the user's message.
    """

    available_races, available_classes, available_backgrounds = get_available_options(db)

    system_prompt = f"""You are an expert in character creation for Dungeons & Dragons.
    Based on the user's message, determine their most likely:
    - Character name
    - Race (Choose from: {', '.join(available_races)})
    - Class (Choose from: {', '.join(available_classes)})
    - Background (Choose from: {', '.join(available_backgrounds)})

    If the input is unclear, use the default: Adventurer Human Ranger Urchin.
    Try to infer Race Class and Background conceptually based on the input but avoid infering a
    name if uncertain.
    Respond with only a JSON object like this:
    {{
        "name": "Arthur"
        "race": "Elf",
        "class": "Wizard",
        "background": "Sage"
    }}
    """

    response = llm_service.generate_one_off_response(system_prompt, user_message)

    try:
        parsed_data = json.loads(response)
        return (
            (parsed_data.get("name", "Adventurer")),
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


def create_character(db: Session, llm_service: LLMService, user_message: str):
    """Handles character creation when a player does not already have one."""
    character_name, race_name, class_name, background_name = parse_character_from_text(
        llm_service, user_message, db
    )

    # Fetch the corresponding database entries
    race = db.query(Race).filter(Race.name == race_name).first()
    char_class = db.query(CharacterClass).filter(CharacterClass.name == class_name).first()
    background = db.query(Background).filter(Background.name == background_name).first()

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
    db.add(character)
    db.commit()
    db.refresh(character)

    return character, race, char_class, background


def get_character_summary(character, race, char_class, background):
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


@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    llm_service: LLMService = Depends(get_llm_service),
    db: Session = Depends(get_db),
):
    """Handles chat interactions and injects character stats into the LLM context."""
    metadata = []  # Stores hidden messages that won't be displayed

    # Prepend initial prompt
    # TODO: On current design we need to prepend initial message every time
    if llm_service.initial_prompt:
        if (
            not request.conversation_history
            or request.conversation_history[0]["content"] != llm_service.initial_prompt
        ):
            request.conversation_history.insert(
                0, {"role": "system", "content": llm_service.initial_prompt}
            )
            logger.info("Initial prompt prepended to conversation history")

    # Initialize character
    if not db.query(Character).first():
        # TODO: When session management is added, replace this with user-specific character lookup
        character, race, char_class, background = create_character(
            db, llm_service, request.user_message
        )

        # Add game context & character details to metadata
        character_summary = get_character_summary(character, race, char_class, background)
        metadata.append(
            {
                "role": "system",
                "content": "Game Context: The Dungeon Master is aware of your character's stats and"
                " abilities.",
            }
        )
        metadata.append({"role": "system", "content": character_summary})

        # Get next prompt and append it to chat history
        chat_response = (
            f"Ah, {character.name}, the world stirs at your arrival, eager to test"
            " your mettle. Tell me, traveler, where does your story begin? In the depths of a"
            "forgotten dungeon, in the bustling streets of a grand city, or upon the windswept"
            "plains of an untamed land?"
        )

        logger.info("Character created")
        return ChatResponse(assistant_message=chat_response, metadata=metadata)

    # Initilize llm service with request conversation history
    llm_service.conversation_history = request.conversation_history

    # Append message to llm chat history and generate next response
    llm_service.conversation_history.append({"role": "user", "content": request.user_message})
    assistant_reply = llm_service.generate_chat_response()

    return ChatResponse(assistant_message=assistant_reply, metadata=metadata)


# Run the server with Uvicorn (if running locally, use `uvicorn main:app --reload`)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
