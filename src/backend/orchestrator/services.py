"""LLM Service Abstraction for DungeonMind.

This module provides an abstraction layer for interacting with various language models (LLMs).
It allows flexibility in switching between different models.
"""

import json
import pathlib
from abc import ABC, abstractmethod

import yaml
from openai import OpenAI

from src.constants import BACKEND_CONFIG, SECRETS


class LLMService(ABC):
    """
    Abstract base class for language model services.

    Args:
        model (str): Model version used for response generation.
        conversation_history (List[Dict[str, str]]): The conversation context.
    """

    def __init__(
        self,
        model: str,
        initial_prompt: str | None,
        conversation_history: list[dict[str, str]] | None = None,
    ):
        self._model = model
        self.initial_prompt = initial_prompt
        if conversation_history:
            self.conversation_history = conversation_history
        else:
            self.conversation_history = []

    @property
    def model(self):
        """Model name is inmutable."""
        return self._model

    @abstractmethod
    def generate_chat_response(self) -> str:
        """
        Generates a response from the language model continuing the chat history.

        Returns:
            str: The model-generated response.
        """

    @abstractmethod
    def generate_one_off_response(self, system_prompt: str, user_input: str) -> str:
        """
        Generates a response from the language model without affecting chat continuity.

        Returns:
            str: The model-generated response.
        """


class OpenAIService(LLMService):
    """
    OpenAI GPT-based language model service.
    """

    def __init__(
        self,
        model: str = "gpt-4",
        initial_prompt: str | None = None,
        temperature: float | None = 0.7,
    ):
        super().__init__(model, initial_prompt)
        self.temperature = temperature

        try:
            with open(SECRETS / "open-ai-creds.json", encoding="utf-8") as f:
                api_key = json.load(f).get("key")
                self.client = OpenAI(api_key=api_key)
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading OpenAI credentials: {e}") from e

    def generate_chat_response(self):
        """Generates a response using the current conversation history."""
        messages = self.conversation_history

        # Get response from current history
        response = (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=self.temperature
            )
            .choices[0]
            .message.content
        )

        return response

    def generate_one_off_response(self, system_prompt: str, user_input: str):
        """Generates a response without modifying conversation history."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]

        response = (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=self.temperature
            )
            .choices[0]
            .message.content
        )

        return response


class SampleService(LLMService):
    """
    Hello world model service for testing conection with the front end.
    """

    def __init__(self, model: str = "sample", initial_prompt: str | None = None):
        super().__init__(model, initial_prompt)

    def generate_chat_response(self):

        return f"(Local AI) You said: {self.conversation_history[-1]['content']}"

    def generate_one_off_response(self, system_prompt: str, user_input: str):
        return f"(Local AI) System was prompted {system_prompt}, user message was {user_input}"


class ModelFactory:
    """
    Factory class to dynamically select the LLM backend based on configuration.
    """

    def __init__(self, llm_backend: str, config_path: pathlib.Path = BACKEND_CONFIG):
        self.llm_backend = llm_backend

        with open(config_path, encoding="utf-8") as file:
            self.backend_config = yaml.safe_load(file)["backends"][self.llm_backend]

    def get_model_service(self) -> LLMService | None:
        """
        Returns an instance of the selected LLM service.

        Args:
            backend (str): The model backend to use.
            temperature (float): Temperature setting for response creativity.

        Returns:
            LLMService: An instance of the chosen model service.
        """
        if self.llm_backend == "chatgptv1":
            openai_service = OpenAIService(
                model=self.backend_config["model"],
                temperature=self.backend_config["temperature"],
                initial_prompt=self.backend_config.get("initial_prompt", None),
            )
            return openai_service

        elif self.llm_backend == "samplev1":
            sample_service = SampleService(
                model=self.backend_config["model"],
                initial_prompt=self.backend_config.get("initial_prompt", None),
            )
            return sample_service
        else:
            raise ValueError(f"Unsupported backend: {self.llm_backend}")
