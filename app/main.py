from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app import models
from app.database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from app import auth
from app.charts import get_chart_data
import json


app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

@app.get('/charts/{topic}')
def get_chart(topic: str):
    try:
        chart_data = get_chart_data(topic)
        if not chart_data:
            raise HTTPException(status_code=404, detail=f"No data found for topic: {topic}")
        return JSONResponse(
            content=chart_data,
            media_type="application/json",
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

@app.post('/survey')
def upload_survey():
    pass

@app.get('/history')
def history(user:user_dependency, db:db_dependency):
    if not auth.get_user_role(user.username, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed')
    survey_result = db.

@app.get('/auth')
def authenticate(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed')
    return {'User': user}
