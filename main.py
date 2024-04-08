from fastapi import FastAPI, status, HTTPException
from schemas import Student,StudentUpdate
from database import students_collection
from bson import ObjectId
from bson.errors import InvalidId

app = FastAPI()

def update(id:str, key, new_value:str|int):
    result = students_collection.find_one_and_update({'_id':ObjectId(id)}, {'$set': {key: new_value}})
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="student not found")
    return result

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

@app.patch('/students/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def update_student(id:str, student:StudentUpdate):
    student_dict = student.model_dump()
    update_query = {}

    if student_dict.get('name'):
        update_query['name'] = student_dict['name']

    if student_dict.get('age'):
        update_query['age'] = student_dict['age']

    if student_dict.get('address'):
        address_dict = student_dict.get('address')
        if address_dict.get('city'):
            update_query['address.city'] = address_dict['city']
        if address_dict.get('country'):
            update_query['address.country'] = address_dict['country']

    try:
        result = students_collection.find_one_and_update({'_id':ObjectId(id)}, {'$set': update_query})
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="student not found")
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid id")
    
    return
    

@app.delete('/students/{id}', status_code=status.HTTP_200_OK)
def delete_student(id:str):
    try:
        result =  students_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="student not found")
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid id")
    return
    