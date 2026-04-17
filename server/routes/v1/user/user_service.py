from routes.v1.user.dto.expert_response import ExpertResponse
from routes.v1.user.dto.user_response import UserResponse
from utils.response.index import ResponseModel
from .user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.socket.index import socket_manager 

class UserService: 

    def __init__(self) : 
        self.user_repository = UserRepository()

    async def find_all(self, db: AsyncSession) -> ResponseModel[List[UserResponse]]: 
        users = await self.user_repository.find_all(db)
        response : ResponseModel[List[UserResponse]] = ResponseModel(
            success=True,
            data=[
                UserResponse(
                    username=user.username,
                    email=user.email,
                    role=user.role
                )
                for user in users
            ],
            message="User data feteched successfully"
        )
        return response

    async def find_by_id(self, user_id, db: AsyncSession) -> ResponseModel[UserResponse]: 
       
        user = await self.user_repository.find_by_id(user_id, db)
        response : ResponseModel[UserResponse] = ResponseModel(
            success=True,
            data=UserResponse(
                username=user.username,
                email=user.email,
                role=user.role
            ),
            message="User retrived successfully"
        )

        return response
        
    async def find_by_email(self, user_email, db: AsyncSession) -> ResponseModel[UserResponse] :
        user = await self.user_repository.find_by_id(user_email, db)
        response : ResponseModel[UserResponse] = ResponseModel(
            success=True,
            data=UserResponse(
                username=user.username,
                email=user.email,
                role=user.role
            ),
            message="User retrived successfully"
        )
        return response

    async def me(self, user_id : int, db : AsyncSession) -> ResponseModel[UserResponse] : 

        user = await self.find_by_id(user_id=user_id, db=db)
        return user

    async def find_experts(self, db : AsyncSession) -> ResponseModel[List[ExpertResponse]] : 

        experts = await self.user_repository.find_experts(db=db)

        response : ResponseModel[List[ExpertResponse]] = ResponseModel(
            success=True,
            data=[
                ExpertResponse(
                    username=expert.username,
                    email=expert.email,
                    role=expert.role,
                    online=socket_manager.is_online(expert.id)
                )
                for expert in experts
            ],
            message="Expert retrived successfully",
            pagination=None
        ) 

        return response
