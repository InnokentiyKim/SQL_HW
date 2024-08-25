from typing import Optional
from pydantic import BaseModel, PositiveInt


class BotUser(BaseModel):
    id: Optional[PositiveInt]
    name: str


class UserSettings(BaseModel):
    id: Optional[PositiveInt]
    notification: Optional[PositiveInt]
    translation_mode: Optional[PositiveInt]


class UserStats(BaseModel):
    id: Optional[PositiveInt]
    number_of_attempts: Optional[PositiveInt]
    successful_attempts: Optional[PositiveInt]
    success_streak: Optional[PositiveInt]


class Word(BaseModel):
    id: Optional[PositiveInt]
    eng_title: str
    rus_title: str
    is_studied: Optional[PositiveInt]
    number_of_attempts: Optional[PositiveInt]
    successful_attempts: Optional[PositiveInt]
    success_streak: Optional[PositiveInt]
    user_id: [PositiveInt]



# class Category(BaseModel):
#     id: Optional[PositiveInt]
#     eng_name: str
#     rus_name: str
#
#
# class CategoryWord(BaseModel):
#     category_id: [PositiveInt]
#     word_id: [PositiveInt]
