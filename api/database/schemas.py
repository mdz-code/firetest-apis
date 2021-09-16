from pydantic import BaseModel
from typing import Optional, List

class UserUpdate(BaseModel):
    email: Optional[str]
    complete_name: Optional[str]
    password: Optional[str]

class UserAuth(BaseModel):
    email: str
    password: str

class UserBase(BaseModel):
    email: str
    complete_name: str

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: str

    class Config:
        orm_mode = True


class PremiumBase(BaseModel):
    is_premium: str
    subscription_date: str

class PremiumCreate(PremiumBase):
    pass

class Premium():
    id: str
    user_id: str

    class Config:
        orm_mode = True

class ObjectInfos(BaseModel):
    years: List[int]
    subjects: List[str]

class SimulateDTO(BaseModel):
    train_mode: bool
    object_infos: ObjectInfos

class Reporter(BaseModel):
    question_id: str
    text_report: str

class QuestionFeedback(BaseModel):
    question_id: str
    correct_answer: bool
    target: str
    score: float


class SimulateBase(BaseModel):
    user_id: str
    questions: List[QuestionFeedback]
    subjects: List[str]
    years: List[str]
    start_time: int
    end_time: int

class RecoverUser(BaseModel):
    email: str