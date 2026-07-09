from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone_number: str = Field(min_length=6, max_length=30)
    city: str | None = Field(default=None, max_length=120)
    bio: str | None = Field(default=None, max_length=1000)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """All fields optional — update any subset of profile fields."""
    name: str | None = Field(default=None, min_length=1, max_length=120)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, min_length=6, max_length=30)
    city: str | None = Field(default=None, max_length=120)
    bio: str | None = Field(default=None, max_length=1000)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone_number: str
    city: str | None
    bio: str | None
    created_at: datetime