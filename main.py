from fastapi import FastAPI, status, HTTPException
from schemas import Student,StudentUpdate
import database as db
from bson.errors import InvalidId

app = FastAPI()
@app.on_event('shutdown')
def shutdown():
    db.close_connection()

@app.post('/students', status_code=status.HTTP_201_CREATED)
async def create_students(student: Student):
    id = db.add_student(student)
    return {'id': id}

@app.get('/students',status_code=status.HTTP_200_OK)
async def list_students(country:str|None = None, age:int|None = None):
    student_list = db.list_students(country, age)
    return {'data': student_list}

@app.get('/students/{id}')
async def fetch_student(id:str):
    try:
        student = db.get_student_by_id(id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid id")
    except db.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"student with id {id} does not exist")
    return student

@app.patch('/students/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def update_student(id:str, student:StudentUpdate):
    try:
        db.update_student_by_id(id, student)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid id")
    except db.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"student with id {id} does not exist")
    return

@app.delete('/students/{id}', status_code=status.HTTP_200_OK)
def delete_student(id:str):
    try:
        db.delete_student_by_id(id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid id")
    except db.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"student with id {id} does not exist")
    return {}
    