# This will be the student schema

from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic import validator
from datetime import datetime
from typing import List, Optional
from core import db
import logging

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return v


class Student(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    name: str
    email: str
    password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    rating: Optional[int] = Field(default=0)
    group_list: Optional[List[str]] = Field(default=[])
    group_limit: Optional[int] = Field(default=5)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PyObjectId: str
        }
    
    @classmethod
    async def create_student(cls, student: 'Student'):
        try:
            student = await db.students.insert_one(student.dict())
            return student
        except Exception as e:
            logging.error(f"Error creating student: {str(e)}")
            raise
    
    async def get_student_by_email(email) -> dict:
        try:
            print(3)
            student = await db.students.find_one({"email": email})
            print(4)
            # convert the student record to a dictionary
            student = dict(student)
            print(5)
            return student
        except Exception as e:
            logging.error(f"Error fetching student by email: {str(e)}")
            raise
    
    class Config:
        json_encoders = {
            ObjectId: str
        }


    def __repr__(self):
        return f'<Student {self.id}>'



class StudentLogin(BaseModel):
    email: str
    password: str

    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v
