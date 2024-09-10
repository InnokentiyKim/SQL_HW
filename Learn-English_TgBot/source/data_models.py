from typing import Optional
from pydantic import BaseModel, PositiveInt


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
    model: Optional[str] = 'Category'
    id: Optional[PositiveInt]
    name: str


class CategoryWordDTO(BaseModel):
    model: Optional[str] = 'CategoryWord'
    category_id: PositiveInt
    word_id: PositiveInt


class WordDTO(BaseModel):
    model: Optional[str] = 'Word'
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
