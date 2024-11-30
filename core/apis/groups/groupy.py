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
            - data: dict containing the created group
    """

    # Attempt to create a new group
    try:
        created_group = await Group.create_group(group)
        print(f" inside group :{created_group}")
        if created_group:

            serialized_group = {
                'id' : str(created_group['id']),
                'name': created_group['name'],
                'feild': created_group['feild'],
                'min_requirement': created_group['min_requirement'],
                'creator_id': created_group['creator_id'],
                'max_limit': created_group['max_limit'],
                'current_capacity': created_group['current_capacity'],
                'created_at': created_group['created_at'].isoformat(),
                'updated_at': created_group['updated_at'].isoformat(),
                'student_list': created_group['student_list'],
                'avg_rating': created_group['avg_rating'],
                'status': created_group['status'],
                'number_of_coadmins': created_group['number_of_coadmins'],
                'number_of_elders': created_group['number_of_elders']
            
            }

            return APIResponse.respond(
                status_code=201,
                status="success",
                message="Group created successfully",
                data={"group": serialized_group}
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