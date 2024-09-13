from typing import Optional
from pydantic import BaseModel, PositiveInt


class TargetWord(BaseModel):
    word_id: Optional[int]
    rus_title: str
    eng_title: str
    is_studied: int
    number_of_attempts: int
    successful_attempts: int
    success_streak: int
    is_answered: int


class BotUserDTO(BaseModel):
    id: PositiveInt
    name: Optional[str]


class UserSettingsDTO(BaseModel):
    id: PositiveInt
    notification: int = 0
    translation_mode: PositiveInt = 1


class UserStatsDTO(BaseModel):
    id: PositiveInt
    number_of_attempts: int = 0
    successful_attempts: int = 0
    success_streak: int = 0


class CategoryDTO(BaseModel):
    id: Optional[PositiveInt]
    name: str


class CategoryWordDTO(BaseModel):
    category_id: PositiveInt
    word_id: PositiveInt


class WordDTO(BaseModel):
    id: Optional[PositiveInt]
    eng_title: str
    rus_title: str
    user_id: PositiveInt


class WordStatsDTO(BaseModel):
    id: PositiveInt
    is_studied: int = 0
    number_of_attempts: int = 0
    successful_attempts: int = 0
    success_streak: int = 0
