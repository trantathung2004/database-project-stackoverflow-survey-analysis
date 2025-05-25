from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal
from typing import Annotated, Dict, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text
import auth
from charts import get_chart_data, get_age_group_stats


app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

@app.get('/charts/{topic}')
def get_chart(topic: str):
    try:
        chart_data = get_chart_data(topic)
        if not chart_data:
            raise HTTPException(status_code=404, detail=f"No data found for topic: {topic}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=chart_data,
            media_type="application/json",
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/age-stats/{question_id}")
def get_age_stats(question_id: int):
    """
    Get age-based statistics for a specific question
    """
    try:
        age_stats = get_age_group_stats(question_id)
        if not age_stats:
            raise HTTPException(status_code=404, detail=f"No data found for question ID: {question_id}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=age_stats,
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
    if not auth.get_user_role(user['username'], db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authorized to access this')
    
    query = text("""
        SELECT * FROM v_history_response
        LIMIT 100
    """)
    results = db.execute(query).mappings().all()
    history =  [dict(row) for row in results]

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=history
        )

@app.get('/auth')
def authenticate(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed')
    return {'User': user}
