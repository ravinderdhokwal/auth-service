from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSignUpRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)

    model_config = ConfigDict(extra="forbid")

class UserSignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)

    model_config = ConfigDict(extra="forbid")

class UserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime