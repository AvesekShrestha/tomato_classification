from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.database.index import  get_db
from routes.v1.user.dto.dashboard_response import DashboardResponse
from routes.v1.user.dto.expert_response import ExpertResponse
from routes.v1.user.dto.user_response import UserResponse
from schemas import user
from utils.errors.index import InternalServerError
from utils.response.index import ResponseModel
from .user_service import UserService
from middlewares.auth_middleware import admin_authorization, current_user_id

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

@router.get("/dashboard")
async def dashboard(db : AsyncSession = Depends(get_db), user_id = Depends(current_user_id)) : 
    try : 
        response : ResponseModel[DashboardResponse] = await user_service.dashboard(user_id=user_id, db=db)
        return response

    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

        
@router.get("/expert", response_model=ResponseModel[List[ExpertResponse]], response_model_exclude_none=True)
async def find_experts(db : AsyncSession = Depends(get_db)) -> ResponseModel[List[ExpertResponse]] : 

    try : 
        response : ResponseModel[List[ExpertResponse]] = await user_service.find_experts(db=db)
        return response
    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.get("/pending-expert", response_model=ResponseModel[List[ExpertResponse]], response_model_exclude_none=True)
async def pending(db : AsyncSession = Depends(get_db), _ = Depends(admin_authorization)) -> ResponseModel[List[ExpertResponse]] : 
    try : 
        response : ResponseModel[List[ExpertResponse]] = await user_service.find_pending_experts(db=db)
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

@router.patch("/{user_id}/approve", response_model=ResponseModel[ExpertResponse], response_model_exclude_none=True)
async def approve_expert(user_id : int, db : AsyncSession = Depends(get_db), _ = Depends(admin_authorization)) -> ResponseModel[ExpertResponse] : 
    try: 
        response = await user_service.approve_expert(user_id=user_id, db=db)
        return response

    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.patch("/{user_id}/reject", response_model=ResponseModel[ExpertResponse], response_model_exclude_none=True)
async def reject_expert(user_id : int, db : AsyncSession = Depends(get_db), _ = Depends(admin_authorization)) -> ResponseModel[ExpertResponse] : 
    try: 
        response = await user_service.reject_expert(user_id=user_id, db=db)
        return response

    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)
