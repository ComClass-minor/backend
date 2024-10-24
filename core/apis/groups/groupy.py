from core import app
from core.models.group import Group
from core.apis.responses import APIResponse
from fastapi import APIRouter, HTTPException, Request , Depends
from core.apis import decorators
import logging

router = APIRouter()

@router.post("/create_group", response_model=APIResponse)
async def create_group(
    group: Group,  # FastAPI automatically handles body parsing
    user: decorators.AuthUser = Depends(decorators.verify_token)  # Inject user via Depends
) -> APIResponse:
    """
    Create a new group.
    
    Args:
        group: Group object containing:
            - name: str
            - field: str
            - min_requirement: int
            - creator_id: str
        user: AuthUser object extracted from the token.

    Returns:
        APIResponse object containing:
            - status_code: int
            - status: str
            - message: str
    """

    # Attempt to create a new group
    try:
        created_group = await Group.create_group(group)
        if created_group:
            return APIResponse.respond(
                status_code=201,
                status="success",
                message="Group created successfully"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to create the group"
            )
    except Exception as e:
        # Log the exception and return a 500 response
        logging.error(f"Error creating group: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
