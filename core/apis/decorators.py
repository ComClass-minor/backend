import json
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

# Authentication class for granting and verifying tokens
class Authenticate:
    def __init__(self, token: str):
        self.token = token

    # Grant a token to the user
    def grant_token(self) -> str:
        return self.token

    # Verify the token
    def verify_token(self, token: str) -> bool:
        return token == self.token

# Dependency to get the token from the request header and verify it
def get_current_token(request: Request, auth: Authenticate = Depends(Authenticate("secret-token"))) -> bool:
    token: Optional[str] = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    if not auth.verify_token(token):
        raise HTTPException(status_code=403, detail="Invalid token")

    return True



