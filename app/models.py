from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from typing import Optional
from pydantic import BaseModel

class Users(Base):
    __tablename__ = 'Users'

    ID = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True)
    hashedpassword = Column(String(255))
    role = Column(String(5))


class Respondents(Base):
    __tablename__ = 'Respondents'

    ResponseID = Column(Integer, primary_key=True, autoincrement=True)
    MainBranch = Column(String(100))
    Age = Column(String(100))
    Country = Column(String(100))
    Employment = Column(String(100))
    EdLevel = Column(String(100))
    UID = Column(Integer)

class Responses(Base):
    __tablename__ = 'Responses'

    ResponseID = Column(Integer, ForeignKey('Respondents.ResponseID'), primary_key=True)
    AnswerID = Column(Integer, primary_key=True)
    QID = Column(Integer, primary_key=True)

class Questions(Base):
    __tablename__ = "Questions"

    QID = Column(Integer, primary_key=True, autoincrement=True)
    qname = Column(String(100), nullable=False, unique=True)
    question = Column(String, nullable=False)
    GID = Column(String(100), nullable=False)

    # Optional: if you have a GroupQuestion model
    # group = relationship("GroupQuestion", back_populates="questions")


class Answers(Base):
    __tablename__ = "Answers"

    AnswerID = Column(Integer, primary_key=True, autoincrement=True)
    Answer = Column(String, nullable=False)

class RespondentCreate(BaseModel):
    Age: Optional[str]
    Country: Optional[str] 
    EdLevel: Optional[str]
    Employment: Optional[str]
    MainBranch: Optional[str]
    LanguageHaveWorkedWith: Optional[str] = None
    LanguageWantToWorkWith: Optional[str] = None
    DatabaseHaveWorkedWith: Optional[str] = None
    DatabaseWantToWorkWith: Optional[str] = None
    WebframeHaveWorkedWith: Optional[str] = None
    WebframeWantToWorkWith: Optional[str] = None
    LearnCode: Optional[str] = None
    LearnCodeOnline: Optional[str] = None
    AISelect: Optional[str] = None
    AIThreat: Optional[str] = None
    AIToolCurrentlyUsing: Optional[str] = None
    OpSysPersonalUse: Optional[str] = None
    OpSysProfessionalUse: Optional[str] = None

class UpdateAnswerRequest(BaseModel):
    qname: str
    new_answer: str