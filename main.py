from fastapi import FastAPI, status, HTTPException
from schemas import Student,StudentUpdate
import database as db


app = FastAPI()

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
    student = db.get_student_by_id(id)
    return student

@app.patch('/students/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def update_student(id:str, student:StudentUpdate):
    db.update_student_by_id(id, student)
    return

@app.delete('/students/{id}', status_code=status.HTTP_200_OK)
def delete_student(id:str):
    db.delete_student_by_id(id)
    return {}
    