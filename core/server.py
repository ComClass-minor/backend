from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from core import app  # Import the FastAPI app from __init__.py
# from core.libs import helpers
from core.apis.student import student_register_router
from core.apis.groups import groupy_router
# from marshmallow.exceptions import ValidationError
import uvicorn

# Include your routes
app.include_router(student_register_router, prefix="/student")
app.include_router(groupy_router, prefix="/group")

# app.include_router(student_assignments_resources, prefix="/student")
# app.include_router(teacher_assignments_resources, prefix="/teacher")
# app.include_router(principal_assignments_resources, prefix="/principal")
# app.include_router(principal_teachers_resources, prefix="/principals")

# @app.get("/")
# async def ready():
#     """
#     Health check endpoint
#     """
#     return {
#         "status": "ready",
#         "time": helpers.get_utc_now()
#     }

# @app.exception_handler(Exception)
# async def handle_exception(request: Request, exc: Exception):
#     """
#     Custom exception handler for different types of exceptions.
#     """
#     if isinstance(exc, FyleError):
#         return JSONResponse(
#             status_code=exc.status_code,
#             content={"error": exc.__class__.__name__, "message": exc.message},
#         )
#     elif isinstance(exc, ValidationError):
#         return JSONResponse(
#             status_code=400,
#             content={"error": exc.__class__.__name__, "message": exc.messages},
#         )
#     elif isinstance(exc, IntegrityError):
#         return JSONResponse(
#             status_code=400,
#             content={"error": exc.__class__.__name__, "message": str(exc.orig)},
#         )
#     elif isinstance(exc, HTTPException):
#         return JSONResponse(
#             status_code=exc.status_code,
#             content={"error": exc.__class__.__name__, "message": str(exc.detail)},
#         )

#     # For all other exceptions, raise a generic HTTPException
#     raise HTTPException(status_code=500, detail="Internal Server Error")

def start():
    """
    This function is responsible for running the Uvicorn server when
    the script is executed directly.
    """
    uvicorn.run("core.server:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    start()
