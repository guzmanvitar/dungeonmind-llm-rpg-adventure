import json

from src.backend.orchestrator.models import ChatRequest
from src.backend.orchestrator.services import LLMServiceFactory
from src.constants import DATA_GAME

CHAT_HISTORY_FILE = DATA_GAME / "active_campaign_chat_history.json"


class GameStateManager:
    """
    Handles chat history storage, retrieval, and summarization to maintain story continuity
    while staying within token limits.
    """

    def __init__(self, backend: str):
        self.summarizer_service = LLMServiceFactory(backend, "story-summarizer").get_service()

    def load_chat_history(self):
        """Loads stored chat history from file if available."""
        if CHAT_HISTORY_FILE.exists():
            with open(CHAT_HISTORY_FILE, encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_chat_history(self, history):
        """Saves chat history to file."""
        with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

    def summarize_history(self, chat_history):
        """
        Summarizes the first 12 non-system messages in the chat history
        to reduce the conversation length while preserving context.
        """
        system_messages = [msg for msg in chat_history if msg["role"] == "system"]
        non_system_messages = [msg for msg in chat_history if msg["role"] != "system"]

        messages_to_summarize = non_system_messages[:-4]

        recent_messages = non_system_messages[-4:]

        if not self.summarizer_service.initial_prompt:
            raise ValueError("Missing system prompt for summarizer service")

        summarizer_prompt = self.summarizer_service.initial_prompt.format(
            chat_log=str(messages_to_summarize),
        )

        summary = self.summarizer_service.generate_formatted_response(summarizer_prompt)

        # Rebuild chat history: Keep system messages, add the summary, and retain last 4 messages
        new_chat_history = system_messages + [{"role": "system", "content": summary}]
        new_chat_history.extend(recent_messages)

        return new_chat_history

    def manage_chat_history(self, request: ChatRequest) -> list:
        """
        Handles chat history storage, retrieval, and summarization to maintain story continuity.

        The function returns a summarized version the history every 12 non-system messages while
        keeping record of full chat history.
        """

        # Load existing chat history
        stored_history = self.load_chat_history()

        # If no chat history initialize with request history
        if not stored_history:
            stored_history = request.conversation_history
        # If chat history exists append new messages
        else:
            stored_history.extend(request.conversation_history[-2:])

        self.save_chat_history(stored_history)

        # Summarize history if needed
        non_system_messages = [
            msg for msg in request.conversation_history if msg["role"] != "system"
        ]
        if len(non_system_messages) >= 16:
            return self.summarize_history(request.conversation_history)
        return request.conversation_history
