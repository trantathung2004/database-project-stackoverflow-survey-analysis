from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal
from typing import Annotated, Dict, List, Tuple
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import auth
from charts import get_chart_data
import audit


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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

@app.post('/upload')
def upload_survey(user: user_dependency, response: models.RespondentCreate, db: db_dependency):
    try:
        respondent = models.Respondents(
            MainBranch=response.MainBranch,
            Age=response.Age,
            Country=response.Country,
            Employment=response.Employment,
            EdLevel=response.EdLevel,
            UID=user['id']
        )
        db.add(respondent)
        db.commit()
        db.refresh(respondent)
        main_q = list(respondent.__dict__.keys())[1:]

        for field_name, answer_text in response.model_dump().items():
            if not answer_text or field_name in main_q:
                continue

            question = db.query(models.Questions).filter_by(qname=field_name).first()
            if not question:
                raise HTTPException(status_code=400, detail=f"Invalid question name: {field_name}")

            answer = db.query(models.Answers).filter_by(Answer=answer_text).first()
            if not answer:
                raise HTTPException(status_code=400, detail=f"Invalid answer: {answer_text}")
            new_response = models.Responses(
                ResponseID=respondent.ResponseID,
                QID=question.QID,
                AnswerID=answer.AnswerID
            )
            db.add(new_response)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Survey uploaded successfully"}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get('/history')
def history(user:user_dependency, db:db_dependency):
    if auth.get_user_role(user['username'], db):
        query = text("""
            SELECT * FROM v_history_response
            ORDER BY ResponseID DESC
            LIMIT 100
        """)
    else:
        query = text(f"""
            SELECT * FROM v_history_response
            WHERE UID = {user['id']}
        """)

    results = db.execute(query).mappings().all()
    history =  [dict(row) for row in results]
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=history
        )


@app.delete('/history/delete')
def delete_submission(user: user_dependency, db: db_dependency):
    respondent = db.query(models.Respondents).filter_by(UID=user['id']).first()
    if not respondent:
        raise HTTPException(status_code=404, detail="No submission found")

    db.query(models.Responses).filter_by(ResponseID=respondent.ResponseID).delete()
    db.query(models.Respondents).filter_by(ResponseID=respondent.ResponseID).delete()
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,  content={"message": "Submission Deleted"})

@app.put('/history/update')
def update_submission(request: models.UpdateAnswerRequest, 
                        user: user_dependency,
                        db: db_dependency):
    print(request.model_dump())
    respondent = db.query(models.Respondents).filter_by(UID=user['id']).first()
    basic_info_qname = list(respondent.__dict__.keys())[1:]
    if not respondent:
        raise HTTPException(status_code=404, detail="Submission not found")

    question = db.query(models.Questions).filter_by(qname=request.qname).first()
    if not question and request.qname in basic_info_qname:
        raise HTTPException(status_code=404, detail="Question not found")

    answer = db.query(models.Answers).filter_by(Answer=request.new_answer).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    response = db.query(models.Responses).filter_by(
        ResponseID=respondent.ResponseID, QID=question.QID
    ).first()
    if not response:
        new_response = models.Responses(ResponseID=respondent.ResponseID, QID=question.QID,AnswerID=answer.AnswerID)
        db.add(new_response)
    elif request.qname in basic_info_qname:
        if hasattr(respondent, request.qname):
            setattr(respondent, request.qname, request.new_answer)
    else:
        response.AnswerID = answer.AnswerID
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Answer updated or added successfully"})

@app.get('/auth')
def authenticate(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed')
    return {'User': user}

@app.get('/audit-logs')
def get_audit_logs(user: user_dependency, db: db_dependency):
    try:
        # Check if user has admin role
        if not auth.get_user_role(user['username'], db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can view audit logs"
            )
            
        logs = audit.get_audit_logs()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=logs,
            media_type="application/json",
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
