import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone_number: str = Field(min_length=6, max_length=10)   # ← 6-10 digits

    city: str | None = Field(default=None, max_length=120)
    bio: str | None = Field(default=None, max_length=1000)

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        errors = []
        if len(v) < 8:
            errors.append("at least 8 characters")
        if not re.search(r"[A-Z]", v):
            errors.append("at least one uppercase letter (A-Z)")
        if not re.search(r"\d", v):
            errors.append("at least one number (0-9)")
        if errors:
            raise ValueError(f"Password must contain: {', '.join(errors)}.")
        return v

    @field_validator("phone_number")
    @classmethod
    def phone_digits_only(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)
        if len(digits) < 6 or len(digits) > 10:
            raise ValueError("Phone number must be 6–10 digits.")
        return digits   # store digits only


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, min_length=6, max_length=10)
    city: str | None = Field(default=None, max_length=120)
    bio: str | None = Field(default=None, max_length=1000)

    @field_validator("phone_number")
    @classmethod
    def phone_digits_only(cls, v: str | None) -> str | None:
        if v is None:
            return v
        digits = re.sub(r"\D", "", v)
        if len(digits) < 6 or len(digits) > 10:
            raise ValueError("Phone number must be 6–10 digits.")
        return digits


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone_number: str
    city: str | None
    bio: str | None
    created_at: datetime