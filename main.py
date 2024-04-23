from fastapi import FastAPI, status, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from schemas import Student,StudentUpdate
import database as db
from bson.errors import InvalidId
import redis 
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title='Task',
              summary='A CRUD app',
              )

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['*'],
                   allow_headers=['*'])

@app.on_event('shutdown')
def shutdown():
    db.close_connection()


r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True)
limit = 100 #100 requests per day from single student
ttl = datetime.timedelta(days=1) #time to live for request count of each student

@app.middleware('http')
async def rate_limit(request:Request, call_next):
    student_id = request.headers.get('X-id') #read custom header X-id
    if not student_id:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":"header field 'X-id' not found"})
    
    #check if student exists
    try:
        db.get_student_by_id(student_id)
    except InvalidId:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail":"invalid student id"})
    except db.NotFound:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"detail":f"student with id {student_id} does not exist"})

    if r.exists(student_id):
        r.incr(student_id) #increment request count
        if int(r.get(student_id)) > limit:
            return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS,content={"detail":f"{limit} requests allowed per day"})
    else:
        r.setex(student_id,time=ttl,value=1) #request count expires after 1 day

    response = await call_next(request)
    return response

@app.post('/students', status_code=status.HTTP_201_CREATED, tags=['Students'])
async def create_students(student: Student):
    id = db.add_student(student)
    return {'id': id}

@app.get('/students',status_code=status.HTTP_200_OK, tags=['Students'])
async def list_students(country:str|None = None, age:int|None = None):
    student_list = db.list_students(country, age)
    return {'data': student_list}

@app.get('/students/{id}', tags=['Students'])
async def fetch_student(id:str):
    try:
        student = db.get_student_by_id(id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid id")
    except db.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"student with id {id} does not exist")
    return student

@app.patch('/students/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
async def update_student(id:str, student:StudentUpdate):
    try:
        db.update_student_by_id(id, student)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid id")
    except db.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"student with id {id} does not exist")
    return

@app.delete('/students/{id}', status_code=status.HTTP_200_OK, tags=['Students'])
def delete_student(id:str):
    try:
        db.delete_student_by_id(id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid id")
    except db.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"student with id {id} does not exist")
    return {}
    