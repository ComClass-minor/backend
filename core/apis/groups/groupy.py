from core import app
from core.models.group import Group
from core.apis.responses import APIResponse
from fastapi import APIRouter, HTTPException, Request , Depends , Body
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


@router.post("/join_group", response_model=APIResponse)
async def join_group(
    group_id: str = Body(...),
    user_id: str = Body(...),
) -> APIResponse:
    """
    Join a group.
    
    Args:
        group_id: str
        user_id: str
        user: AuthUser object extracted from the token.

    Returns:
        APIResponse object containing:
            - status_code: int
            - status: str
            - message: str
    """

    # Attempt to join the group
    try:
        joined_group = await Group.join_group(group_id, user_id)
        if joined_group:
            return APIResponse.respond(
                status_code=200,
                status="success",
                message="Joined group successfully"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to join the group"
            )
    except Exception as e:
        # Log the exception and return a 500 response
        logging.error(f"Error joining group: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.post("/leave_group", response_model=APIResponse)
async def leave_group( group_id: str = Body(...), user_id: str = Body(...), ) -> APIResponse:
    """
    Leave a group.
    Args:
        group_id: str
        user_id: str
        user: AuthUser object extracted from the token.
    Returns:
        APIResponse object containing:
            - status_code: int
            - status: str
            - message: str
    """

    # Attempt to leave the group
    try:
        left_group = await Group.leave_group(group_id, user_id)
        if left_group:
            return APIResponse.respond(
                status_code=200,
                status="success",
                message="Left group successfully"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to leave the group"
            )
    except Exception as e:
        # Log the exception and return a 500 response
        logging.error(f"Error leaving group: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )