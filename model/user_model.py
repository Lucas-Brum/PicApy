from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
