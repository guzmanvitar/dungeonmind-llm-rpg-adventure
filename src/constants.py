"""Defines project constants"""

from pathlib import Path

this = Path(__file__)

ROOT = this.parents[1]

LOGS = ROOT / "logs"

SRC = ROOT / "src"

BACKEND = SRC / "backend"

BACKEND_CONFIG = BACKEND / "llm-services-config.yaml"

SECRETS = ROOT / ".secrets"

DATA = ROOT / "data"
DATA_RAW = DATA / "raw"
DATA_PROCESSED = DATA / "processed"

DATABASE = ROOT / ".db"
DATABASE_FAISS = DATABASE / "faiss"

MODELS = ROOT / "models"

TESTS_DIR = ROOT / "tests"

LOGS.mkdir(exist_ok=True, parents=True)
DATA_RAW.mkdir(exist_ok=True, parents=True)
DATA_PROCESSED.mkdir(exist_ok=True, parents=True)
MODELS.mkdir(exist_ok=True)
DATABASE.mkdir(exist_ok=True)
