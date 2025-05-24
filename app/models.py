from app.database import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = 'Users'

    ID = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True)
    hashedpassword = Column(String(255))
    role = Column(String(5))

class Questions(Base):
    __tablename__ = 'Questions'

    QID = Column(Integer, primary_key=True, index=True)
    qname = Column(String(100), unique=True)
    

class Responses(Base):
    __tablename__ = 'Responses'

