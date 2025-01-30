"""LLM Service Abstraction for DungeonMind.

This module provides an abstraction layer for interacting with various language models (LLMs).
It allows flexibility in switching between  different models.
"""

import os
from abc import ABC, abstractmethod

import openai


class LLMService(ABC):
    """
    Abstract base class for language model services.
    """

    @abstractmethod
    def generate_response(
        self, conversation_history: list[dict[str, str]], user_message: str
    ) -> str:
        """
        Generates a response from the language model.

        Args:
            conversation_history (List[Dict[str, str]]): The conversation context.
            user_message (str): The user's latest input.

        Returns:
            str: The model-generated response.
        """


class OpenAIService(LLMService):
    """
    OpenAI GPT-based language model service.
    """

    def __init__(self, model: str = "gpt-4", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature
        openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")

    def generate_response(
        self, conversation_history: list[dict[str, str]], user_message: str
    ) -> str:
        messages = conversation_history + [{"role": "user", "content": user_message}]

        response = openai.ChatCompletion.create(
            model=self.model, messages=messages, temperature=self.temperature
        )

        return response["choices"][0]["message"]["content"]


class SampleService(LLMService):
    """
    Example of a locally hosted language model service.
    """

    def generate_response(
        self, conversation_history: list[dict[str, str]], user_message: str
    ) -> str:
        # Placeholder: Implement connection to a local Llama model
        return f"(Local AI) You said: {user_message}"


class ModelFactory:
    """
    Factory class to dynamically select the LLM backend based on configuration.
    """

    @staticmethod
    def get_model_service(model_name: str = "openai") -> LLMService:
        """
        Returns an instance of the selected LLM service.

        Args:
            model_name (str): The model backend to use. Default is "openai".

        Returns:
            LLMService: An instance of the chosen model service.
        """
        if model_name == "openai":
            return OpenAIService()
        elif model_name == "sample":
            return SampleService()
        else:
            raise ValueError(f"Unsupported model: {model_name}")
