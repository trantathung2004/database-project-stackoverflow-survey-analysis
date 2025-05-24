from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import auth


app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

@app.get('/charts/{topic}')
def get_chart(topic:str):
    topic = 'learncode'
    response = dict()
    #key qname, values [('answertext', %)]
    pass

@app.get('/history')
def history():
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/auth',)
def authenticate(user: None, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Failed')
    return {'User': user}

@app.post('/register')
def register():
    pass