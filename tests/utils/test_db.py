from pydantic import PostgresDsn
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from app.core.config import settings

SQLALCHEMY_TEST_DATABASE_URL = PostgresDsn.build(
    scheme="postgresql",
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    path=f"/{settings.TEST_DB_NAME}",
)
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
