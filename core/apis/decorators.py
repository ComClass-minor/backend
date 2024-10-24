from functools import wraps
from fastapi import HTTPException, Request
import jwt
import logging
from datetime import datetime
from typing import Callable, Any
from core import SECRET_KEY
from pydantic import BaseModel



class AuthUser(BaseModel):
    email: str
    exp: datetime


def accept_payload(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
        try:
            # Parse JSON body from the request
            incoming_payload = await request.json()
            # Pass the payload explicitly if it's not already in kwargs
            kwargs['payload'] = incoming_payload  # Always pass payload
            return await func(request, *args, **kwargs)
        except Exception as e:
            logging.error(f"Error reading payload: {e}")
            raise HTTPException(status_code=400, detail="Invalid payload format")
    return wrapper


def verify_token(request: Request) -> AuthUser:
    try:
        # Extract the token from the request headers
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Token is missing")

        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Check for necessary fields in the payload
        email = payload.get("email")
        exp = payload.get("exp")

        if email is None or exp is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        # Create AuthUser instance using Pydantic validation
        return AuthUser(email=email, exp=exp)

    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError as e:
        logging.error(f"Token error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
