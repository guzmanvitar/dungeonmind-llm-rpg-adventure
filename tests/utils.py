"""Utils for project wide testing"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.backend.database.models import Base
from src.backend.database.populate_db import bulk_insert


def get_mock_db():
    """
    Creates and returns an in-memory SQLite mock database session.
    Ensures tables are created and pre-populated with test data.
    """
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    mock_db = testing_session_local()
    Base.metadata.create_all(bind=engine)

    # Populate the mock database
    bulk_insert(mock_db)

    return mock_db
