from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URI')
client = MongoClient(DATABASE_URL)
lms_db = client.lib_management_system
students_collection = lms_db.students
