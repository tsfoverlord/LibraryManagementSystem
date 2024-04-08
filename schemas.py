from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    city:str
    country:str

class StudentOut(BaseModel):
    name:str
    age:int

class Student(StudentOut):
    address:Address

class AddressUpdate(BaseModel):
    city:str|None = None
    country:str|None = None

class StudentUpdate(BaseModel):
    name:str | None = None
    age:int|None = None
    address: AddressUpdate|None = None

