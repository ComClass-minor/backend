# Here we will adjust for the blog posts 

from pydantic import BaseModel , Field, validator
from bson import ObjectId
from core import db
from datetime import datetime
from core.libs import assertions
from typing import List, Optional
import logging
from core.models.student import Student
from fastapi import HTTPException


class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, handler):
        if not isinstance(value, ObjectId):
            if not ObjectId.is_valid(str(value)):
                raise ValueError("Invalid ObjectId")
            value = ObjectId(str(value))
        return str(value)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")
        return field_schema

class Blog(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    author_id: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    total_likes: Optional[int] = Field(default=0)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        },
        "json_schema_extra": {
            "example": {
                "_id": "64f12345b789c12345d67890",
                "title": "Sample Blog",
                "content": "Sample content",
                "author_id": "sample_author_id",
                "created_at": "2023-01-01T00:00:00",
                "total_likes": 0
            }
        }
    }

    def to_json(self):
        """Convert the model to JSON, properly handling ObjectId and datetime."""
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "total_likes": self.total_likes
        }

    @classmethod
    async def create_blog(cls, blog: 'Blog') -> 'Blog':
        """
        This method creates a blog post
        params:
            blog: Blog: The blog object
            {
                "title": "string",
                "content": "string",
                "author_id": "string"
            }
        returns:
            Blog: The blog object
            {
                "id": "string",
                "title": "string",
                "content": "string",
                "author_id": "string",
                "created_at": "datetime",
                "total_likes": "int"
            }
        """
        try:
            author = await Student.get_student_by_id(blog.author_id)
            if not author:
                raise HTTPException(status_code=404, detail=f"Author with author id : {blog.author_id} is not found")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
        return await db.blogs.insert_one(blog.dict())
    
    @staticmethod
    async def get_blog_by_user(author_id: str) -> List['Blog']:
        """
        This method gets all blog posts by a user
        params:
            author_id: str: The author id
        returns:
            List[Blog]: The list of blog posts
        """
        try:
            author = await Student.get_student_by_id(author_id)
            assertions.assert_not_found(author, "Author not found")
            # now we get all the blog posts by the author
            blogs = await db.blogs.find({"author_id": author_id}).to_list(length=100)
            return blogs
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
    
    @staticmethod
    async def remove_blog(blog_id: str) -> bool:
        """
        This method removes a blog post
        params:
            blog_id: str: The blog id
        returns:
            bool: True if successful, False otherwise
        """
        try:
            blog = await db.blogs.find_one({"_id": ObjectId(blog_id)})
            assertions.assert_not_found(blog, "Blog not found")
            await db.blogs.delete_one({"_id": ObjectId(blog_id)})
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        
    @staticmethod
    async def like_blog(blog_id: str , Auther_id: str) -> bool:
        """
        This method likes a blog post
        params:
            blog_id: str: The blog id
        returns:
            bool: True if successful, False otherwise
        """
        try:
            blog = await db.blogs.find_one({"_id": ObjectId(blog_id)})
            assertions.assert_not_found(blog, "Blog not found")
            user = await Student.get_student_by_id(Auther_id)
            assertions.assert_not_found(user, "User not found")
            # now we update the total likes
            await db.blogs.update_one({"_id": ObjectId(blog_id)}, {"$inc": {"total_likes": 1}})
            return True
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
    