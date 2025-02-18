"""Backend utils functions"""

from src.backend.database.config import SessionLocal


def get_db():
    """Dependency to get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
