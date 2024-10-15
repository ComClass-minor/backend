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
    async def get_student_by_email(cls, email: str):
        try:
            student = await db.students.find_one({"email": email})
            return student
        except Exception as e:
            logging.error(f"Error querying the database: {str(e)}")
            raise
    
    @classmethod
    async def create_student(cls, student: 'Student'):
        try:
            student = await db.students.insert_one(student.dict())
            return student
        except Exception as e:
            logging.error(f"Error creating student: {str(e)}")
            raise

    def __repr__(self):
        return f'<Student {self.id}>'
