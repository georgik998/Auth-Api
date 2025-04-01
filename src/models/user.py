from enum import Enum
from pydantic import BaseModel, Field


class UserSexEnum(Enum):
    male = 'm'
    female = 'f'
