from pydantic import BaseModel, Field
from enum import Enum

from src.models.user import UserSexEnum


class RegistrationData(BaseModel):
    phone_number: str = Field(max_length=21)
    email: str = Field(max_length=64)
    password: str
    sex: UserSexEnum
    full_name: str = Field(max_length=64)


class ConfirmCodeData(BaseModel):
    code: str
    registration_code_key: str


class LoginData(BaseModel):
    email: str = Field(max_length=64)
    password: str


class JwtTokenType(Enum):
    access = 'access'
    refresh = 'refresh'


class ResetPasswordData(BaseModel):
    email: str = Field(max_length=64)


class NewPasswordData(BaseModel):
    password: str
    token: str
