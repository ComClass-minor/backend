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
    student_list: Optional[List[str]] = Field(default=[])
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
        try:
            print(group)
            creator = await Student.get_student_by_id(group.creator_id)
            assertions.assert_not_found(creator, "Creator not found")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
        print(creator)
        assertions.assert_bad_request(creator['group_limit'] > 1, "User has reached the group limit")
        if creator['rating']: print(creator['rating'])
        # assertions.assert_bad_request(creator['rating'] > group.min_requirement, "Cannot create group as user rating is less than the minimum requirement")
        try:
            print(1)
            group = await db.groups.insert_one(group.dict())
            # group.avg_rating = creator['rating']
            #  we need to update the creator's group list
            creator['group_list'] = creator['group_list'].append({str(group.inserted_id): "Admin"})
            creator['group_limit'] = creator['group_limit'] - 1
            await Student.update_student(creator)

            return group
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
    
