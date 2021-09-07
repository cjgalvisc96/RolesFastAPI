from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import create_database, database_exists

from app.api.deps import get_db
from app.db.base import Base
from app.db.init_db import init_db
from app.main import app
from tests.utils.overrides import override_get_db
from tests.utils.test_db import (
    SQLALCHEMY_TEST_DATABASE_URL,
    TestingSessionLocal,
    engine
)
from tests.utils.user import (
    authentication_token_from_email,
    get_superadmin_token_headers,
    regular_user_email
)


@pytest.fixture(scope="session")
def db() -> Generator:
    if not database_exists(SQLALCHEMY_TEST_DATABASE_URL):
        create_database(SQLALCHEMY_TEST_DATABASE_URL)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal()

@pytest.fixture(autouse=True)
def create_initial_db_data_test(db: Session) -> None:
    init_db(db)

@pytest.fixture(scope="module")
def client() -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture()
def superadmin_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superadmin_token_headers(client=client)


@pytest.fixture()
def normal_user_token_headers(
    client: TestClient, db: Session
) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=regular_user_email, db=db
    )
