from core import app
from core.models.group import Group
from core.apis.responses import APIResponse
from fastapi import APIRouter, HTTPException, Depends
from core.apis import decorators

router = APIRouter()

@router.post("/create_group", response_model=APIResponse)
@decorators.validate_token
async def create_group(group: Group) -> APIResponse:
    """
    Create a new group
    Args:
        group: Group object
        {
            "name": str,
            "feild": str,
            "min_requirement": int,
            "creator_id": str
        }
    
    Returns:
        APIResponse object
        {
            "status_code": int,
            "status": str,
            "message": str
        }
    """

    # Create a new group
    group = await Group.create_group(group)
    if group:
        return APIResponse.respond(
            status_code=201,
            status="success",
            message="Group created successfully"
        )
    else:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
