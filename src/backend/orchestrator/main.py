"""
FastAPI orchestrator for the DungeonMind project.

This module provides an API for handling chat interactions with a language model (LLM).
It processes user input, maintains conversation history, and generates AI-driven responses.
"""

from functools import partial

import yaml
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.backend.database.config import SessionLocal
from src.backend.database.models import Character
from src.backend.game_dynamics.character_creation import CharacterManager
from src.backend.orchestrator.models import ChatRequest, ChatResponse
from src.backend.orchestrator.routes.character import router as character_router
from src.backend.orchestrator.services import LLMService, LLMServiceFactory
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


# Get db and llm services
def get_llm_service(service_type: str) -> LLMService | None:
    """Dependency injection for selecting the LLM service."""
    # Initialize LLMServiceFactory with selected backend
    with open(BACKEND_CONFIG, encoding="utf-8") as file:
        selected_backend = yaml.safe_load(file).get("selected_backend", "samplev1")

    model_factory = LLMServiceFactory(selected_backend, service_type)
    llm_service = model_factory.get_service()

    return llm_service


def get_db():
    """Dependency to get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    dungeon_master: LLMService = Depends(partial(get_llm_service, "dungeon-master")),
    character_creator: LLMService = Depends(partial(get_llm_service, "character-creation")),
    db: Session = Depends(get_db),
):
    """Handles chat interactions and injects character stats into the LLM context."""
    metadata = []  # Stores hidden messages that won't be displayed

    # Initialize character
    if not db.query(Character).first():
        # TODO: When session management is added, replace this with user-specific character lookup
        character_manager = CharacterManager(db, character_creator)

        character, race, char_class, background = character_manager.create_character(
            request.user_message
        )

        # Add game context & character details to metadata
        character_summary = character_manager.get_character_summary(
            character, race, char_class, background
        )
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

    # Initilize dungeon master service with request conversation history
    dungeon_master.conversation_history = (
        dungeon_master.conversation_history + request.conversation_history
    )

    # Append message to llm chat history and generate next response
    dungeon_master.conversation_history.append({"role": "user", "content": request.user_message})
    assistant_reply = dungeon_master.chat_completion()

    return ChatResponse(assistant_message=assistant_reply, metadata=metadata)


# Run the server with Uvicorn (if running locally, use `uvicorn main:app --reload`)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
