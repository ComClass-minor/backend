from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Optional

app = FastAPI()

class APIResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None  # Optional field to hold response data
    status_code: Optional[int] = None  # Optional field for HTTP status code

    @classmethod
    def respond(cls, status_code: int, status: str, message: str, data: Optional[Any] = None) -> 'APIResponse':
        return cls(
            status=status,
            message=message,
            data=data,
            status_code=status_code
        )
