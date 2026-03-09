from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.database.index import  get_db
from routes.v1.user.dto.user_response import UserResponse
from utils.errors.index import InternalServerError
from utils.response.index import ResponseModel
from .user_service import UserService

router = APIRouter()
user_service = UserService()

@router.get("/")
async def get_all(db : AsyncSession = Depends(get_db)) -> ResponseModel[List[UserResponse]] : 
    try : 
        response = await user_service.find_all(db)
        return ResponseModel[List[UserResponse]](success=True, data=response, message="User data feteched successfully")

    except Exception as e : 
        error_message = e.args[0]
        raise InternalServerError(error_message)

@router.get("/{user_id}")
async def get_by_id(user_id : int, db : AsyncSession = Depends(get_db)) -> ResponseModel[UserResponse] : 
    try : 
        response = await user_service.find_by_id(user_id, db)
        return ResponseModel[UserResponse](success=True, data=response, message="User data feteched successfully")

    except Exception as e : 
        error_message = e.args[0]
        raise InternalServerError(error_message)
