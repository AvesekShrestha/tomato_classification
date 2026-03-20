from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database.index import get_db
from middlewares.auth_middleware import current_user_id
from routes.v1.post.comment.dto.comment_request import CommentRequest
from routes.v1.post.comment.dto.comment_response import CommentResponse
from utils.errors.index import InternalServerError
from .comment_service import CommentService
from utils.response.index import ResponseModel

router = APIRouter()
comment_service = CommentService()


@router.get("/", response_model=ResponseModel[List[CommentResponse]], response_model_exclude_none=True)
async def get_by_post_id(post_id : int, db : AsyncSession = Depends(get_db)) -> ResponseModel[List[CommentResponse]] :

    try:
        response : List[CommentResponse] = await comment_service.find_by_post_id(post_id=post_id, db=db)
        return ResponseModel[List[CommentResponse]](
            success=True,
            data=response,
            message="Comment reterived successfully"
        )
    except Exception as e: 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.get("/{comment_id}", response_model=ResponseModel[CommentResponse], response_model_exclude_none=True)
async def get_by_id(comment_id : int, db : AsyncSession = Depends(get_db)):
    try:
        response : CommentResponse = await comment_service.find_by_id(comment_id=comment_id, db=db)
        return ResponseModel[CommentResponse](
            success=True,
            data=response,
            message="Comment reterived successfully"
        )
    except Exception as e: 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.post("/", response_model=ResponseModel[CommentResponse], response_model_exclude_none=True)
async def create(payload : CommentRequest, post_id : int, user_id : int = Depends(current_user_id), db : AsyncSession = Depends(get_db)) -> ResponseModel[CommentResponse]: 

    try:
        response : CommentResponse = await comment_service.create(payload=payload, post_id=post_id, user_id=user_id, db=db)
        return ResponseModel[CommentResponse](
            success=True,
            data=response,
            message="Comment created successfully"
        )

    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.get("/{comment_id}/reply", response_model=ResponseModel[List[CommentResponse]], response_model_exclude_none=True)
async def get_reply(comment_id : int, db : AsyncSession = Depends(get_db)) : 
    try:
        response : List[CommentResponse] = await comment_service.get_reply(comment_id=comment_id, db=db)
        return ResponseModel[List[CommentResponse]](
            success=True,
            data=response,
            message="replies reterived successfully"
        )

    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.post("/{comment_id}/reply", response_model_exclude_none=True, response_model=ResponseModel[CommentResponse])
async def reply(payload : CommentRequest, post_id : int, comment_id : int, user_id : int = Depends(current_user_id), db : AsyncSession = Depends(get_db)) :
    try :
        response : CommentResponse = await comment_service.reply(payload=payload, post_id=post_id, comment_id=comment_id, user_id=user_id, db=db)

        return ResponseModel[CommentResponse](
            success=True,
            data=response,
            message="Reply created successfully"
        )
    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.post("/{comment_id}/like", response_model_exclude_none=True, response_model=ResponseModel[CommentResponse])
async def like(comment_id : int, user_id : int = Depends(current_user_id), db : AsyncSession = Depends(get_db)) -> ResponseModel[CommentResponse] : 
    try : 
        response : CommentResponse = await comment_service.like(comment_id=comment_id, user_id=user_id, db=db)
        return ResponseModel[CommentResponse](
            success=True,
            data=response,
            message="Post liked successfully"
        )
    except Exception as e : 
        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.post("/{comment_id}/dislike", response_model_exclude_none=True, response_model=ResponseModel[CommentResponse])
async def dislike(comment_id : int, user_id : int = Depends(current_user_id), db : AsyncSession = Depends(get_db)) -> ResponseModel[CommentResponse] : 
    try : 
        response : CommentResponse = await comment_service.dislike(comment_id=comment_id, user_id=user_id, db=db)
        return ResponseModel[CommentResponse](
            success=True,
            data=response,
            message="Post disliked successfully"
        )

    except Exception as e : 
        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.delete("/{comment_id}", response_model=ResponseModel[None], response_model_exclude_none=True)
async def delete(comment_id : int, user_id : int = Depends(current_user_id), db : AsyncSession = Depends(get_db)) -> ResponseModel[CommentResponse] :
    try:
        await comment_service.delete(comment_id=comment_id, user_id=user_id, db=db)
        return ResponseModel[CommentResponse](
            success=True,
            data=None,
            message="Comment deleted successfully"
        )

    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

