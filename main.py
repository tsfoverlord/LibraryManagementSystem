from fastapi import FastAPI, status, HTTPException
from schemas import Student,StudentUpdate
from database import students_collection
from bson import ObjectId
from bson.errors import InvalidId

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
async def fetch_student(id:str):
    try:
        result = students_collection.find(filter = {'_id':ObjectId(id)}, projection={'_id':0})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid id")
    if result.retrieved == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="student not found")
    return result.next()

@app.patch('/students/{id}')
async def update_student(id:str, student:StudentUpdate):

    pass

@app.delete('/students/{id}')
def delete_student():
    pass