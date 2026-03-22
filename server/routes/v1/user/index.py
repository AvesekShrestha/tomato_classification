from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.database.index import  get_db
from routes.v1.user.dto.user_response import UserResponse
from utils.errors.index import InternalServerError
from utils.response.index import ResponseModel
from .user_service import UserService
from middlewares.auth_middleware import current_user_id

router = APIRouter()
user_service = UserService()

@router.get("/")
async def get_all(db : AsyncSession = Depends(get_db)) -> ResponseModel[List[UserResponse]] : 
    try : 
        response : ResponseModel[List[UserResponse]] = await user_service.find_all(db)
        return response

    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.get("/me", response_model=ResponseModel[UserResponse], response_model_exclude_none=True)
async def me(db : AsyncSession = Depends(get_db), user_id = Depends(current_user_id)) -> ResponseModel[UserResponse] : 

    try : 
        response : ResponseModel[UserResponse]  = await user_service.me(user_id=user_id, db=db)
        return response
        
    except Exception as e :
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.get("/{user_id}")
async def get_by_id(user_id : int, db : AsyncSession = Depends(get_db)) -> ResponseModel[UserResponse] : 
    try : 
        response = await user_service.find_by_id(user_id, db)
        return response

    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)


