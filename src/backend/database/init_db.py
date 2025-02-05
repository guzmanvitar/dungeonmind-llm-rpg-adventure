"""Initializes game database."""

from src.backend.database.config import engine
from src.backend.database.models import Base


def initialize_db():
    """Creates all tables based on SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    initialize_db()
