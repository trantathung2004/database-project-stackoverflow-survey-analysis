from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Users(Base):
    __tablename__ = 'Users'

    ID = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True)
    hashedpassword = Column(String(255))
    role = Column(String(5))


class Respondent(Base):
    __tablename__ = 'Respondents'

    ResponseID = Column(Integer, primary_key=True, autoincrement=True)
    MainBranch = Column(String(100))
    Age = Column(String(100))
    Country = Column(String(100))
    Employment = Column(String(100))
    EdLevel = Column(String(100))

class Response(Base):
    __tablename__ = 'Responses'

    ResponseID = Column(Integer, ForeignKey('Respondents.ResponseID'), primary_key=True)
    AnswerID = Column(Integer, primary_key=True)
    QID = Column(Integer, primary_key=True)