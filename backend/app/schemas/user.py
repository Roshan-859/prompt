from datetime import datetime
from typing import Optional
import re
from pydantic import BaseModel, ConfigDict, field_validator


def normalize_and_validate_email(v: str) -> str:
    cleaned = v.strip().lower()
    # Flexible email regex accepting all standard domains including gmail, outlook, custom domains, etc.
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, cleaned):
        raise ValueError("Please provide a valid email address (e.g. yourname@gmail.com)")
    return cleaned


class UserBase(BaseModel):
    email: str
    full_name: str
    role: str = "student"

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        return normalize_and_validate_email(v)


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserRead


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        return normalize_and_validate_email(v)


class RefreshRequest(BaseModel):
    refresh_token: str
