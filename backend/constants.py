"""Defines backend constants"""

from pathlib import Path

this = Path(__file__)

ROOT = this.parents[1]

BACKEND = ROOT / "backend"

BACKEND_CONFIG = BACKEND / "llm-backend-config.yaml"

SECRETS = ROOT / ".secrets"
