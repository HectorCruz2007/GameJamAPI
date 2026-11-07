from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.config import DATABASE_URL

# check_same_thread is required when SQLite is used by FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
