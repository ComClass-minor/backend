# This will be the student schema

from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic import validator
from datetime import datetime
from typing import List, Optional
from core import db
from core.libs import assertions
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
    async def create_student(cls, student: 'Student') -> 'Student':
        """
        This is a classmethod for Student and as the name suggests, it is used to create a new student record in the database.
        param: student: Student object
            student: Student Object : {
                "user_id": str,
                "name": str,
                "email": str,
                "password": str,
                }
        return: student: Student Object
            {
                "user_id": str,
                "name": str,
                "email": str,
                "password": str,
                "created_at": datetime,
                "updated_at": datetime,
                "rating": int,
                "group_list": List[str],
                "group_limit": int
            }
        """ 
        try:
            student = await db.students.insert_one(student.dict())
            return student 
        except Exception as e:
            logging.error(f"Error creating student: {str(e)}")
            raise
    
    @classmethod
    async def update_student(cls, student: 'Student') -> 'Student':
        """
        This is a classmethod for Student and as the name suggests, it is used to update a student record in the database.
        param: student: Student object
            student: Student Object : {
                "user_id": str,
                "name": str,
                "email": str,
                "password": str,
                "created_at": datetime,
                "updated_at": datetime,
                "rating": int,
                "group_list": List[str],
                "group_limit": int
            }
        
        return: student: Student Object
            {
                "user_id": str,
                "name": str,
                "email": str,
                "password": str,
                "created_at": datetime,
                "updated_at": datetime,
                "rating": int,
                "group_list": List[str],
                "group_limit": int
            }
        """
        try:
            student['updated_at'] = datetime.now()
            student = await db.students.update_one({"user_id": student['user_id']}, {"$set": student})
            return student
        except Exception as e:
            logging.error(f"Error updating student: {str(e)}")
            raise

    
    @staticmethod
    async def get_student_by_id(id: str) -> 'Student':
        """
        This is not a classmethod, but a static method. It is used to fetch a student record from the database by id.
        param: id: str
        returns student: Student Object
        """
        try:
            student = await db.students.find_one({"user_id": id})
            assertions.assert_not_found(student, "Student not found")
            return student
        except Exception as e:
            logging.error(f"Error fetching student by id: {str(e)}")
            raise


    @staticmethod
    async def get_student_by_email(email : str) -> 'Student':
        """
        This is not a classmethod, but a static method. It is used to fetch a student record from the database by email.
        param: email: str
        returns student: Student Object
        """
        try:
            student = await db.students.find_one({"email": email})
            assertions.assert_not_found(student, "Student not found")
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