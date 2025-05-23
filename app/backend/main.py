from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


app = FastAPI()

@app.get('/charts/{topic}')
def get_chart(topic:str):
    topic = 'learncode'
    response = dict()
    #key qname, values [('answertext', %)]
    pass

@app.get('/history')
def history():
    pass

@app.get('/login')
def login():
    pass

@app.post('/register')
def register():
    pass