from pydantic import BaseModel
from typing import Optional, List


# USER_INFOS 

class UserInfos(BaseModel):
    schooling: str
    institution: str
    user_id: Optional[str]

class UserInfosUpdate(BaseModel):
    schooling: Optional[str]
    institution: Optional[str]

# USER

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

class UserDTO(BaseModel):
    account: UserCreate
    infos: UserInfos

class UserDTOUpdate(BaseModel):
    account: UserUpdate
    infos: Optional[UserInfosUpdate]

# RECOVER 
class RecoverUser(BaseModel):
    email: str

# PREMIUM

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

# REPORTER

class Reporter(BaseModel):
    question_id: str
    text_report: str

# FEEDBACKS

class FeedbackRegister(BaseModel):
    question_id: str
    correct: bool
    feedback: str

class QuestionFeedback(BaseModel):
    question_id: str
    correct_answer: bool
    target: str
    score: float

class QuestionFeedbackDocument(BaseModel):
    question_id: str
    datetime: str

class ReviewFeedbackDocument(BaseModel):
    subject_id: str
    start_at: str

class UsersFeedbackDocument(BaseModel):
    user_id: str
    correct_answer: List[QuestionFeedbackDocument]
    wrong_answer: List[QuestionFeedbackDocument]
    hard: List[QuestionFeedbackDocument]
    medium: List[QuestionFeedbackDocument]
    easy: List[QuestionFeedbackDocument]
    to_review: List[ReviewFeedbackDocument]

# SIMULATES

class ObjectInfos(BaseModel):
    years: List[int]
    subjects: List[str]

class SimulateBase(BaseModel):
    user_id: str
    questions: List[QuestionFeedback]
    subjects: List[str]
    years: List[str]
    start_time: int
    end_time: int

class SimulateDTO(BaseModel):
    train_mode: bool
    object_infos: ObjectInfos