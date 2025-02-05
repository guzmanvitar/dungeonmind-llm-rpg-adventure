"""Defines project constants"""

from pathlib import Path

this = Path(__file__)

ROOT = this.parents[1]

LOGS = ROOT / "logs"

SRC = ROOT / "src"

BACKEND = SRC / "backend"

BACKEND_CONFIG = BACKEND / "llm-backend-config.yaml"

SECRETS = ROOT / ".secrets"

LOGS.mkdir(exist_ok=True, parents=True)
