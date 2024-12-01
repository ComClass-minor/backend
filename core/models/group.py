from pydantic import BaseModel, Field, validator
from bson import ObjectId
from datetime import datetime
from typing import List, Optional
from core import db
import logging
from core.models.student import Student
from core.libs import assertions


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return v


class Group(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    feild: str
    min_requirement: int
    creator_id: str
    max_limit: Optional[int] = Field(default=10)
    current_capacity: Optional[int] = Field(default=0)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    student_list: Optional[List[dict]] = Field(default=[])
    avg_rating: Optional[float] = Field(default=0.0)
    status: Optional[str] = Field(default="active")
    number_of_coadmins: Optional[int] = Field(default=0)
    number_of_elders: Optional[int] = Field(default=0)

    def __init__(self, **data):
        super().__init__(**data)
        self.number_of_coadmins = self.max_limit//10
        self.number_of_elders = self.max_limit//5

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PyObjectId: str
        }
    
    @classmethod
    async def create_group(cls, group: 'Group') -> 'Group':
        """
        params:
            group: Group{
                name: str,
                feild: str,
                min_requirement: int,
                creator_id: str,
                max_limit: int,
                current_capacity: int,
                created_at: datetime,
                updated_at: datetime,
                student_list: List[dict],
                avg_rating: float,
                status: str,
                number_of_coadmins: int,
                number_of_elders: int
            }
        """
        try:
            creator = await Student.get_student_by_id(group.creator_id)
            assertions.assert_not_found(creator, "Creator not found")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
        assertions.assert_bad_request(creator['group_limit'] > 0, "User has reached the group limit")
        if creator['rating']: print(creator['rating'])
        try:
            group.student_list += [{group.creator_id : "Admin"}]
            gid = str(group.id)
            creator['group_list'] = [{ gid: "Admin" }]
            creator['group_limit'] = creator['group_limit'] - 1
            creator.pop('_id', None)
            creator.pop('id', None)
            await Student.update_student(creator)
            group = await db.groups.insert_one(group.dict())
            inserted_id = group.inserted_id
            group_document = await db.groups.find_one({"_id": inserted_id})
            return group_document
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
    

    @staticmethod
    async def join_group(group_id: str, student_id: str) -> bool:
        try:
            # First, print out all debugging information
            print(f"Attempting to join group with ID: {group_id}")
            print(f"Student ID: {student_id}")

            # Check if group_id is a valid ObjectId
            try:
                object_group_id = ObjectId(group_id)
            except Exception as id_error:
                print(f"Invalid ObjectId conversion: {id_error}")
                return False

            # Find the group
            group = await db.groups.find_one({"_id": object_group_id})
            
            # Additional debugging
            print(f"Group found: {group}")
            if not group:
                print(f"No group found with ID: {group_id}")
            return False
            student = await Student.get_student_by_id(student_id)
            assertions.assert_not_found(student, f"Student not found with id: {student_id}")
            group['student_list'] += [{str(student_id): "Member"}]
            student['group_list'] += [{group_id: "Member"}]
            await db.groups.update_one({"_id": ObjectId(group_id)}, {"$set": group})
            await Student.update_student(student)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
    

    @staticmethod
    async def leave_group(group_id: str, student_id: str) -> bool:
        try:
            group = await db.groups.find_one({"_id": ObjectId(group_id)})
            assertions.assert_not_found(group, "Group not found")
            student = await Student.get_student_by_id(student_id)
            assertions.assert_not_found(student, "Student not found")
            group['student_list'] = [ i for i in group['student_list'] if i.get(student_id) not in ["Member", "Admin", "Elder", "Coadmin"]]
            await db.groups.update_one({"_id": ObjectId(group_id)}, {"$set": group})
            student['group_list'] = [group for group in student['group_list'] if group.get(group_id) not in ["Member", "Admin", "Elder", "Coadmin"]]
            student['group_limit'] = student['group_limit'] + 1
            await Student.update_student(student)
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
    
    def __repr__(self):
        return f'<Group {self.id}>'

