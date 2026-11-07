from datetime import date

from sqlmodel import Field, SQLModel


# Database tables


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password_hash: str


class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    platform: str
    hours_played: int
    rating: int
    start_date: date
    completed: bool
    user_id: int = Field(foreign_key="user.id", index=True)
