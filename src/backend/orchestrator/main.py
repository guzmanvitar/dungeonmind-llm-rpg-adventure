"""
FastAPI orchestrator for the DungeonMind project.

This module provides an API for handling chat interactions with a language model (LLM).
It processes user input, maintains conversation history, and generates AI-driven responses.
"""

from functools import partial

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.backend.database.models import Character
from src.backend.game_dynamics.campaign_creation import CampaignManager
from src.backend.game_dynamics.character_creation import CharacterManager
from src.backend.game_dynamics.game_state_manager import GameStateManager
from src.backend.orchestrator.models import ChatRequest, ChatResponse
from src.backend.orchestrator.routes.character import router as character_router
from src.backend.orchestrator.services import LLMService, LLMServiceFactory
from src.backend.utils import get_db
from src.constants import DATA_GAME
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


def get_llm_service(backend: str, service_type: str) -> LLMService | None:
    """Dependency injection for selecting the LLM service."""
    # Initialize LLMServiceFactory with selected backend
    service_factory = LLMServiceFactory(backend, service_type)
    llm_service = service_factory.get_service()

    return llm_service


@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    dungeon_master: LLMService = Depends(partial(get_llm_service, "gpt-4", "dungeon-master")),
    db: Session = Depends(get_db),
):
    """Handles chat interactions and injects character stats into the LLM context."""
    # Initialize character
    if not db.query(Character).first():
        character_manager = CharacterManager(db, "gpt3-5")
        return character_manager.initialize_character(request)

    # Initialize story
    current_campaign_dir = DATA_GAME / "active_campaign.txt"
    if not current_campaign_dir.exists():
        campaign_manager = CampaignManager("gpt-4")
        return campaign_manager.initialize_campaign(request)

    # Manage chat history & summarization
    game_state_manager = GameStateManager("gpt-4")
    current_history = game_state_manager.manage_chat_history(request)
    print(current_history)

    # Initilize dungeon master service with conversation history
    dungeon_master.conversation_history = current_history

    # Generate next response
    assistant_reply = dungeon_master.chat_completion()

    return ChatResponse(
        assistant_message=assistant_reply, metadata=[], conversation_history=current_history
    )


# Run the server with Uvicorn (if running locally, use `uvicorn main:app --reload`)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
