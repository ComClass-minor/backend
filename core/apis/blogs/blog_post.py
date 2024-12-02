from core import app
from core.models.blogs import Blog
from core.apis.responses import APIResponse
from fastapi import APIRouter, HTTPException, Request , Depends , Body , Query
from core.apis import decorators
from datetime import datetime
import logging

router = APIRouter()

@router.post("/create_blog", response_model=APIResponse)
async def create_blog(
    blog: Blog,  # FastAPI automatically handles body parsing
    user: decorators.AuthUser = Depends(decorators.verify_token)  # Inject user via Depends
) -> APIResponse:
    """
    Create a new blog.
    Args:
        blog: Blog object containing:
            - title: str
            - content: str
            - author_id: str
        user: AuthUser object extracted from the token.
    Returns:
        APIResponse object containing:
            - status_code: int
            - status: str
            - message: str
    """
    try:
        created_blog = await Blog.create_blog(blog)
        if created_blog:
            return APIResponse.respond(
                status_code=201,
                status="success",
                message="Blog created successfully"
            )

        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to create the blog"
            )
    # except HTTPException as e:
    #     raise e
    except Exception as e:
        # Log the exception and return a 500 response
        logging.error(f"Error creating blog: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.get("/get_blogs", response_model=APIResponse)
async def get_blogs(author_id: str = Query(..., description="Author ID to fetch blogs for")) -> APIResponse:
    try:
        blogs = await Blog.get_blog_by_user(author_id)
        if blogs:
            # Convert MongoDB documents to Pydantic models
            blog_list = [Blog.model_validate(blog) for blog in blogs]
            return APIResponse(
                status_code=200,
                status="success",
                message="Blogs retrieved successfully",
                data=[blog.to_json() for blog in blog_list]  # Use to_json() for proper serialization
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="No blogs found for this author"
            )
    except Exception as e:
        logging.error(f"Error retrieving blogs: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.put("/like_blog", response_model=APIResponse)
async def like_blog( blog_id: str = Body(...) , user_id: str = Body(...)) -> APIResponse:
    """
    Like a blog.
    Args:
        blog_id: str
        user_id: str
    Returns:
        APIResponse object containing:
            - status_code: int
            - status: str
            - message: str
    """
    try:
        liked_blog = await Blog.like_blog(blog_id, user_id)
        if liked_blog:
            return APIResponse.respond(
                status_code=200,
                status="success",
                message="Blog liked successfully"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to like the blog"
            )
    except Exception as e:
        # Log the exception and return a 500 response
        logging.error(f"Error liking blog: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
    
@router.delete("/remove_blog", response_model=APIResponse)
async def remove_blog(blog_id: str = Body(..., embed=True)) -> APIResponse:
    """
    Remove a blog.
    Args:
        blog_id: str
    Returns:
        APIResponse object containing:
            - status_code: int
            - status: str
            - message: str
    """
    try:
        removed_blog = await Blog.remove_blog(blog_id)
        if removed_blog:
            return APIResponse.respond(
                status_code=200,
                status="success",
                message="Blog removed successfully",
                data={
                    "blog_id": blog_id,
                    "deleted_at": datetime.now()
                }
                )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to remove the blog"
            )
    except Exception as e:
        # Log the exception and return a 500 response
        logging.error(f"Error removing blog: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
