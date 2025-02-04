"""Defines backend constants"""

from pathlib import Path

this = Path(__file__)

ROOT = this.parents[2]

SRC = ROOT / "src"

BACKEND = SRC / "backend"

BACKEND_CONFIG = BACKEND / "llm-backend-config.yaml"

SECRETS = ROOT / ".secrets"
