"""
FastAPI orchestrator for the DungeonMind project.

This module provides an API for handling chat interactions with a language model (LLM).
It processes user input, maintains conversation history, and generates AI-driven responses.
"""

import os

from fastapi import Depends, FastAPI

from backend.orchestrator.models import ChatRequest, ChatResponse
from backend.orchestrator.services import LLMService, ModelFactory

# Initialize FastAPI app
app = FastAPI()


def get_llm_service() -> LLMService:
    """
    Dependency injection for selecting the LLM service.
    Reads the preferred model from environment variables.
    """
    model_name = os.getenv("LLM_BACKEND", "openai")  # Default to OpenAI
    return ModelFactory.get_model_service(model_name)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, llm_service: LLMService = Depends(get_llm_service)):
    """
    Handles chat interactions by sending user input and conversation history to the LLM.
    """
    assistant_reply = llm_service.generate_response(
        request.conversation_history, request.user_message
    )
    return ChatResponse(assistant_message=assistant_reply)


# Run the server with Uvicorn (if running locally, use `uvicorn filename:app --reload`)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
