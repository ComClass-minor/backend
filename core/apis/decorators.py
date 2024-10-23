from functools import wraps
from typing import Optional, Dict, Any
from fastapi import HTTPException, Request
import jwt
import logging
from datetime import datetime


class TokenValidator:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify and decode JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Dict containing token payload
            
        Raises:
            HTTPException: If token is invalid, expired, or malformed
        """
        try:
            # Decode token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Extract email (assuming email is in token payload)
            email = payload.get('email')
            if not email:
                logging.error("Token missing email claim")
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token format"
                )

            # Check expiration
            exp = payload.get('exp')
            if exp and datetime.now().timestamp() > exp:
                logging.error(f"Token expired for user: {email}")
                raise HTTPException(
                    status_code=401,
                    detail="Token has expired"
                )

            return payload

        except jwt.ExpiredSignatureError:
            logging.error("Token has expired")
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )
            
        except jwt.JWTClaimsError:
            logging.error("Invalid token claims")
            raise HTTPException(
                status_code=401,
                detail="Invalid token claims"
            )
            
        except jwt.JWTError:
            logging.error("Invalid token format or signature")
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
            
        except Exception as e:
            logging.error(f"Unexpected error validating token: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error processing token"
            )
    


