from fastapi import FastAPI, status, HTTPException
from schemas import Student
from database import students_collection
app = FastAPI()

dummy_db = []

@app.post('/students', status_code=status.HTTP_201_CREATED)
async def create_students(student: Student):
    result = students_collection.insert_one(student.model_dump())
    return {'id': str(result.inserted_id)}

@app.get('/students')
async def list_students():
    pass


@app.get('/students/{id}')
async def fetch_student():
    pass

@app.patch('/students/{id}')
async def update_student():
    pass

@app.delete('/students/{id}')
def delete_student():
    pass