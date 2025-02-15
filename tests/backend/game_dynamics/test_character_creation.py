"""Testing module for the Character Creation LLM service"""

import json
from pathlib import Path

import pytest
import yaml

from src.backend.game_dynamics.character_creation import CharacterManager
from src.backend.orchestrator.services import LLMServiceFactory
from src.logger_definition import get_logger
from tests.utils import get_mock_db

logger = get_logger(__file__)

TEST_CONFIG_DIR = Path(__file__).resolve().parent

# Load test cases from YAML
with open(TEST_CONFIG_DIR / "character_creation_tests.yaml", encoding="utf-8") as file:
    test_cases = yaml.safe_load(file)["tests"]

# Get in-memory SQLite test database
mock_db = get_mock_db()


@pytest.mark.parametrize("test_case", test_cases)
def test_parse_character_from_text(test_case):
    """
    Tests `parse_character_from_text` using exact match and LLM-based evaluation.
    """
    # Initialize character_manager llm service
    character_creator = LLMServiceFactory("gpt3-5", "character-creation").get_service()
    if not character_creator:
        raise ValueError("Character service creation failed")

    character_manager = CharacterManager(mock_db, character_creator)

    # Load test input and expected values
    input_text = test_case["prompt"]
    expected_output = test_case["expected"]["value"]
    evaluation_type = test_case["expected"]["match"]

    # Generate output from CharacterManager
    actual_output = character_manager.parse_character_from_text(input_text)

    if evaluation_type == "exact":
        assert actual_output == json.loads(
            expected_output
        ), f"Exact match failed: {test_case['description']}"

    elif evaluation_type == "llm":
        # Build LLM tester servie
        tester = LLMServiceFactory("gpt-4", "prompt-tester").get_service()

        if not tester.initial_prompt:
            raise ValueError("Missing system prompt for tester service")

        test = tester.initial_prompt.format(
            expected_output=expected_output, actual_output=actual_output
        )

        response = tester.generate_formatted_response(test).strip().lower()

        assert response.startswith(
            "yes"
        ), f"LLM output evaluation failed. Output: {actual_output} \n Response: {response}"


if __name__ == "__main__":
    pytest.main(["-v", "tests/test_character_manager.py"])
