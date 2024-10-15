# here we will log in the student 

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from core import app
from core.models.student import Student
from core.apis.responses import APIResponse
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import secrets
import logging
# import IntegrityError

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ASSESSION_EXPIRE_MINUTES = 60

def verify_password(plain_password , hashed_password):
    """
    Verify the password of the student by comparing the plain password with the hashed password stored in the database
    """
    return pwd_context.verify(plain_password, hashed_password) 

def create_jwt_token(data : dict , expire_time : timedelta = timedelta(minutes=ASSESSION_EXPIRE_MINUTES)):
    """
    Create a JWT token for the student
    """
    new_data = data.copy()
    expire = datetime.now() + expire_time
    new_data.update({"exp":expire})
    encoded_jwt = jwt.encode(new_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signin" , response_model=APIResponse)
async def signin(student : Student):
    """
    Sign in the student
    """
    try:
        student_record = await Student.get_student_by_email(student.email)
        if student_record:
            if verify_password(student.password, student_record["password"]):
                token = create_jwt_token({"email":student.email})
                return APIResponse.respond(
                    status_code=200,
                    status="success",
                    message="Student signed in successfully",
                    data={"token":token , "student":student_record}
                )
            else:
                return APIResponse.respond(
                    status_code=401,
                    status="error",
                    message="password"
                )
        else:
            return APIResponse.respond(
                status_code=404,
                status="error",
                message="Student not found"
            )
    except Exception as e:
        print(e)
        return APIResponse.respond(
            status_code=500,
            status="error",
            message="Internal server error"
        )
    

@router.post("/signup", response_model=APIResponse)
async def signup(student: Student):
    """
    Sign up the student
    """
    try:
        # Check if the student with this email already exists

        student_record = await Student.get_student_by_email(student.email)
        logging.error(f"Student record type: {type(student_record)}")

        if student_record:
            return APIResponse.respond(
                status_code=409,
                status="error",
                message="Email already in use"
            )
        
        # Hash the password before storing
        student.password = pwd_context.hash(student.password)

        # Create a new student record
        student_record = await Student.create_student(student)
        
        # Create JWT token
        token = create_jwt_token({"email": student.email})

        # Serialize student data, excluding the password
        serialized_student = student_record.dict(exclude={"password"}, by_alias=True)  

        return APIResponse.respond(
            status_code=201,
            status="success",
            message="Student signed up successfully",
            data={"token": token, "student": serialized_student}
        )

    except ValueError as ve:
        logging.error(f"Value error during signup: {str(ve)}")
        return APIResponse.respond(
            status_code=400,
            status="error",
            message=f"Validation error: {str(ve)}"
        )
    # except IntegrityError as ie:  # Example of catching a specific exception
    #     logging.error(f"Integrity error during signup: {str(ie)}")
    #     return APIResponse.respond(
    #         status_code=400,
    #         status="error",
    #         message="Database integrity error"
    #     )
    except Exception as e:
        logging.error(f"Error during signup: {str(e)}")
        return APIResponse.respond(
            status_code=500,
            status="error",
            message="Internal server error"
        )
