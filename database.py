from pymongo import MongoClient
import os
from dotenv import load_dotenv
from schemas import Student, StudentUpdate
from bson import ObjectId
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
client = MongoClient(DATABASE_URL)
lms_db = client.lib_management_system
students_collection = lms_db.students

def add_student(student: Student)-> str:
    result = students_collection.insert_one(student.model_dump())
    return str(result.inserted_id)

def list_students(country:str|None = None, age:int|None = None)-> list:
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
    return student_list

def get_student_by_id(id:str):
    result = students_collection.find(filter = {'_id':ObjectId(id)}, projection={'_id':0})
    student = result.next()
    result.close()
    return student

def update_student_by_id(id:str, fields_to_update:StudentUpdate)->None:
    student_dict = fields_to_update.model_dump()
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

    result = students_collection.find_one_and_update({'_id':ObjectId(id)}, {'$set': update_query})

def delete_student_by_id(id:str)->None:
    result = students_collection.delete_one({'_id': ObjectId(id)})
