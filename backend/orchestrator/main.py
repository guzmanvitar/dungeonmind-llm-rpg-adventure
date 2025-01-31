"""
FastAPI orchestrator for the DungeonMind project.

This module provides an API for handling chat interactions with a language model (LLM).
It processes user input, maintains conversation history, and generates AI-driven responses.
"""

import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.constants import BACKEND_CONFIG
from backend.orchestrator.models import ChatRequest, ChatResponse
from backend.orchestrator.services import ModelFactory

# Initialize FastAPI app
app = FastAPI(docs_url="/")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ModelFactory with selected backend
with open(BACKEND_CONFIG, encoding="utf-8") as file:
    selected_backend = yaml.safe_load(file).get("selected_backend", "samplev1")

model_factory = ModelFactory(selected_backend)
llm_service = model_factory.get_model_service()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Handles chat interactions by sending user input and conversation history to the LLM.
    """
    if not llm_service:
        return ChatResponse(assistant_message="Error: LLM Service not initialized.")

    llm_service.conversation_history.append({"role": "user", "content": request.user_message})
    assistant_reply = llm_service.generate_response()
    llm_service.conversation_history.append({"role": "assistant", "content": assistant_reply})

    return ChatResponse(assistant_message=assistant_reply)


# Run the server with Uvicorn (if running locally, use `uvicorn main:app --reload`)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
