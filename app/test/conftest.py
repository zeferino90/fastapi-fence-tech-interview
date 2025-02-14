import os

import pytest
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from app.main import get_db, app
from database.database_creation import engine
from database.models import Item, create_db_and_tables


TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@pytest.fixture()
def initialize_db(scope="function") -> None:
    create_db_and_tables()

    yield

    SQLModel.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session_fixture(initialize_db)-> Session:
    from sqlmodel import inspect
    print("Before table creation:", inspect(engine).get_table_names())
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function", autouse=True)
def override_get_db(db_session_fixture: Session) -> None:
    def _override_get_db() -> Session:
        return db_session_fixture
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()
