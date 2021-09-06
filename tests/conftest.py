from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy_utils import create_database, database_exists

from app.api.deps import get_db
from app.db.base import Base
from app.main import app
from tests.utils.overrides import override_get_db
from tests.utils.test_db import (
    SQLALCHEMY_TEST_DATABASE_URL,
    TestingSessionLocal,
    engine
)


@pytest.fixture(scope="session")
def db() -> Generator:
    if not database_exists(SQLALCHEMY_TEST_DATABASE_URL):
        create_database(SQLALCHEMY_TEST_DATABASE_URL)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
