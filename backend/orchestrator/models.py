""" Defines the data models used in the backend.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Represents a chat request from the frontend.

    Attributes:
        user_message (str): The user's input message.
        conversation_history (List[Dict[str, str]]): The chat history including system and assistant
        messages.
    """

    user_message: str
    conversation_history: list[dict[str, str]]


class ChatResponse(BaseModel):
    """
    Represents the chatbot's response.

    Attributes:
        assistant_message (str): The AI-generated response.
    """

    assistant_message: str
