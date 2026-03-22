from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from config.database.index import get_db
from middlewares.auth_middleware import current_user_id
from routes.v1.post.dto.post_request import PostRequest
from routes.v1.post.dto.post_response import PostResponse
from utils.errors.index import InternalServerError
from .post_service import PostService
from utils.response.index import ResponseModel
from typing import List
from .comment.index import router as comment_router


router =  APIRouter()
post_service = PostService()

@router.get("/user", response_model=ResponseModel[List[PostResponse]], response_model_exclude_none=True)
async def find_by_user_id(cursor : str | None = None, limit : int = 10, user_id : int = Depends(current_user_id), db : AsyncSession = Depends(get_db)) -> ResponseModel[List[PostResponse]] : 

    try:
        response : ResponseModel[List[PostResponse]] = await post_service.find_by_user_id(limit=limit, cursor=cursor, user_id=user_id, db=db)
        return response
    except Exception as e : 
        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)



@router.get("/", response_model=ResponseModel[List[PostResponse]], response_model_exclude_none=True)
async def find_all(limit : int = 10, cursor : str | None = None, db : AsyncSession = Depends(get_db)) -> ResponseModel[List[PostResponse]] : 
    try :
        response : ResponseModel[List[PostResponse]] = await post_service.find_all(limit=limit, cursor=cursor, db=db)
        return response

    except Exception as e : 
        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)


@router.get("/{post_id}", response_model=ResponseModel[PostResponse], response_model_exclude_none=True)
async def find_by_id(post_id : int, db : AsyncSession = Depends(get_db)) -> ResponseModel[PostResponse] : 
    
    try:
        response : ResponseModel[PostResponse] = await post_service.find_by_id(post_id=post_id, db=db)
        return response
    except Exception as e : 
        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.post("/", response_model=ResponseModel[PostResponse] , response_model_exclude_none=True)
async def create(title : str = Form(...), content : str = Form(...), image : UploadFile = File(None), user_id : int = Depends(current_user_id), db : AsyncSession = Depends(get_db)) -> ResponseModel[PostResponse] : 
    try :
        payload : PostRequest = PostRequest(
            title=title,
            content=content,
            image=image
        )
        response : ResponseModel[PostResponse] = await post_service.create(payload=payload, user_id=user_id, db=db)
        return response

    except Exception as e: 
        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.post("/{post_id}/like", response_model_exclude_none=True, response_model=ResponseModel[PostResponse])
async def like(post_id : int, user_id : int = Depends(current_user_id), db : AsyncSession = Depends(get_db)) -> ResponseModel[PostResponse] : 
    try : 
        response : ResponseModel[PostResponse] = await post_service.like(post_id=post_id, user_id=user_id, db=db)
        return response

    except Exception as e : 
        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.post("/{post_id}/dislike", response_model_exclude_none=True, response_model=ResponseModel[PostResponse])
async def dislike(post_id : int, user_id : int = Depends(current_user_id), db : AsyncSession = Depends(get_db)) -> ResponseModel[PostResponse] : 
    try : 
        response : ResponseModel[PostResponse] = await post_service.dislike(post_id=post_id, user_id=user_id, db=db)
        return response

    except Exception as e : 
        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)


@router.delete("/{post_id}", response_model=ResponseModel[None], response_model_exclude_none=True)
async def delete(post_id : int, db : AsyncSession = Depends(get_db)) -> ResponseModel[None] : 
    
    try : 
        response : ResponseModel[None] = await post_service.delete(post_id=post_id, db=db)
        return response

    except Exception as e : 
        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

router.include_router(comment_router, prefix="/{post_id}/comment")
