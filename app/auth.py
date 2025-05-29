from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from database import SessionLocal
from models import Users
import re
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '' 
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def is_strong_password(password: str) -> bool:
    """
    Check if the password is strong.
    Criteria: At least 8 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character.
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,
                      create_user_request:CreateUserRequest):
    usrname = db.query(Users).filter(Users.username == create_user_request.username).first()
    if usrname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Check password strength
    if not is_strong_password(create_user_request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long and include at least uppercase letter and lowercase letter and digit"
        )
    
    create_user_model = Users(
        username=create_user_request.username,
        hashedpassword=bcrypt_context.hash(create_user_request.password),
        role='user'
    )
    db.add(create_user_model)
    db.commit()

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    if not re.match(r'^[a-zA-Z0-9_-]+$', form_data.username):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong username or password')
    
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong username or password')
    token = create_access_token(user.username, user.ID)
    return {'access_token': token, 'token_type': 'bearer'}

def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashedpassword):
        return False
    return user

def create_access_token(username, id):
    encode = {'sub': username, 'id': id}
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get('sub')
        uid = payload.get('id')
        if username is None or uid is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
        return {'username': username, 'id': uid}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    
def get_user_role(username, db):
    user = db.query(Users).filter(Users.username == username).first()
    if user.role.strip() == 'admin':
        return True
    return False