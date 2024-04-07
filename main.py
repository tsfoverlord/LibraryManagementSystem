from fastapi import FastAPI, status, HTTPException
from schemas import Student,StudentOut
from database import students_collection
app = FastAPI()

dummy_db = []

@app.post('/students', status_code=status.HTTP_201_CREATED)
async def create_students(student: Student):
    result = students_collection.insert_one(student.model_dump())
    return {'id': str(result.inserted_id)}

@app.get('/students',status_code=status.HTTP_200_OK)
async def list_students(country:str|None = None, age:int|None = None):
    project = {
        '_id': 0, 
        'name': 1, 
        'age': 1
    }

    filter = {}
    if country:
        filter.update({'address.country':{'$eq':country}})
    if age:
        filter.update({'age':{'$gte':age}})

    student_list = list(students_collection.find(filter=filter, projection=project))

    return {'data': student_list}



@app.get('/students/{id}')
async def fetch_student():
    pass

@app.patch('/students/{id}')
async def update_student():
    pass

@app.delete('/students/{id}')
def delete_student():
    pass