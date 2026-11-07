from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pydantic.alias_generators import to_camel


# Base for JSON in camelCase, matching the Android DTOs
class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class RegisterRequest(CamelModel):
    name: str = Field(min_length=1, max_length=60)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)  # bcrypt limit


class LoginRequest(CamelModel):
    email: EmailStr
    password: str


class UserResponse(CamelModel):
    id: int
    name: str
    email: str


class AuthResponse(CamelModel):
    access_token: str
    user: UserResponse


class GameRequest(CamelModel):
    title: str = Field(min_length=1, max_length=60)
    platform: str = Field(min_length=1, max_length=40)
    hours_played: int = Field(ge=0)
    rating: int = Field(ge=1, le=10)
    start_date: date
    completed: bool

    @field_validator("title", "platform")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @field_validator("start_date")
    @classmethod
    def not_in_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("must not be in the future")
        return value


class GameResponse(CamelModel):
    id: int
    title: str
    platform: str
    hours_played: int
    rating: int
    start_date: date
    completed: bool
