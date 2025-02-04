"""LLM Service Abstraction for DungeonMind.

This module provides an abstraction layer for interacting with various language models (LLMs).
It allows flexibility in switching between different models.
"""

import json
import pathlib
from abc import ABC, abstractmethod

import yaml
from openai import OpenAI

from src.backend.constants import BACKEND_CONFIG, SECRETS


class LLMService(ABC):
    """
    Abstract base class for language model services.

    Args:
        model (str): Model version used for response generation.
        conversation_history (List[Dict[str, str]]): The conversation context.
    """

    def __init__(self, model: str, conversation_history: list[dict[str, str]] | None = None):
        self._model = model
        if conversation_history:
            self.conversation_history = conversation_history
        else:
            self.conversation_history = []

    @property
    def model(self):
        """Model name is inmutable."""
        return self._model

    @abstractmethod
    def generate_response(self) -> str:
        """
        Generates a response from the language model.

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
        temperature: float | None = 0.7,
    ):
        super().__init__(model)
        self.temperature = temperature

        try:
            with open(SECRETS / "open-ai-creds.json", encoding="utf-8") as f:
                api_key = json.load(f).get("key")
                self.client = OpenAI(api_key=api_key)
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading OpenAI credentials: {e}") from e

    def generate_response(self):
        messages = self.conversation_history

        response = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=self.temperature
        )

        return response.choices[0].message.content


class SampleService(LLMService):
    """
    Hello world model service for testing conection with the front end.
    """

    def __init__(self, model: str = "sample"):
        super().__init__(model)

    def generate_response(self):
        return f"(Local AI) You said: {self.conversation_history[-1]['content']}"


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
        initial_prompt = self.backend_config.get("initial_prompt", None)

        if self.llm_backend == "chatgptv1":
            openai_service = OpenAIService(
                model=self.backend_config["model"],
                temperature=self.backend_config["temperature"],
            )
            if initial_prompt:
                openai_service.conversation_history.append(
                    {"role": "system", "content": initial_prompt}
                )
            return openai_service

        elif self.llm_backend == "samplev1":
            sample_service = SampleService()
            if initial_prompt:
                sample_service.conversation_history.append(
                    {"role": "system", "content": initial_prompt}
                )
            return sample_service
        else:
            raise ValueError(f"Unsupported backend: {self.llm_backend}")
