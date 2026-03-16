from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from config.database.index import get_db
from middlewares.auth_middleware import authenticate
from routes.v1.post.dto.post_request import PostRequest
from routes.v1.post.dto.post_response import PostResponse
from .post_service import PostService
from utils.response.index import ResponseModel
from typing import List


router =  APIRouter()
post_service = PostService()

@router.get("/", response_model=ResponseModel[List[PostResponse]], response_model_exclude_none=True)
async def find_all(db : AsyncSession = Depends(get_db)) -> ResponseModel[List[PostResponse]] : 
    try :
        response : List[PostResponse] = await post_service.find_all(db=db)
        return ResponseModel[List[PostResponse]](
            success=True,
            data=response,
            message="Posts reterived successfully"
        )

    except Exception as e : 
        raise e


@router.get("/{post_id}", response_model=ResponseModel[PostResponse], response_model_exclude_none=True)
async def find_by_id(post_id : int, db : AsyncSession = Depends(get_db)) -> ResponseModel[PostResponse] : 
    
    try:
        response : PostResponse = await post_service.find_by_id(post_id=post_id, db=db)
        return ResponseModel[PostResponse](
            success=True,
            data=response,
            message="Post data retrived successfully"
        )
    except Exception as e : 
        raise e

@router.post("/", response_model=ResponseModel[PostResponse] , response_model_exclude_none=True)
async def create(title : str = Form(...), content : str = Form(...), image : UploadFile = File(None), user_id : int = Depends(authenticate), db : AsyncSession = Depends(get_db)) -> ResponseModel[PostResponse] : 
    try : 
        payload : PostRequest = PostRequest(
            title=title,
            content=content,
            image=image
        )
        response : PostResponse = await post_service.create(payload=payload, user_id=user_id, db=db)
        return ResponseModel[PostResponse](
            success=True,
            data=response,
            message="post created successfully"
        )

    except Exception as e: 
        raise e

@router.delete("/{post_id}", response_model=ResponseModel[None], response_model_exclude_none=True)
async def delete(post_id : int, db : AsyncSession = Depends(get_db)) -> ResponseModel[None] : 
    
    try : 
        await post_service.delete(post_id=post_id, db=db)
        return ResponseModel[None](
            success=True,
            data=None,
            message="Post deleted successfully"
        )

    except Exception as e : 
        raise e
