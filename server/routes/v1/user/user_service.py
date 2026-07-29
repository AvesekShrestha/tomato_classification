from routes.v1.user.dto.dashboard_response import AdminDashboardResponse, ExpertDashboardResponse,FramerDashboardResponse
from routes.v1.user.dto.expert_response import ExpertResponse
from routes.v1.user.dto.user_response import UserResponse
from schemas.user import UserStatus
from utils.errors.index import NotFound
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
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    role=user.role,
                    online=socket_manager.is_online(user.id)
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
                id=user.id,
                username=user.username,
                email=user.email,
                role=user.role,
                online=socket_manager.is_online(user.id)
            ),
            message="User retrived successfully"
        )

        return response
        
    async def find_by_email(self, user_email, db: AsyncSession) -> ResponseModel[UserResponse] :
        user = await self.user_repository.find_by_id(user_email, db)
        response : ResponseModel[UserResponse] = ResponseModel(
            success=True,
            data=UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                role=user.role,
                online=socket_manager.is_online(user.id)
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
                    id=expert.id,
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
    async def find_pending_experts(self, db : AsyncSession) -> ResponseModel[List[ExpertResponse]] : 

            experts = await self.user_repository.find_pending_experts(db=db)

            response : ResponseModel[List[ExpertResponse]] = ResponseModel(
                success=True,
                data=[
                    ExpertResponse(
                        username=expert.username,
                        email=expert.email,
                        role=expert.role,
                        id=expert.id,
                        online=socket_manager.is_online(expert.id)
                    )
                    for expert in experts
                ],
                message="Expert retrived successfully",
                pagination=None
            ) 

            return response

    async def approve_expert(self, user_id : int, db : AsyncSession) -> ResponseModel[ExpertResponse] : 

        expert = await self.user_repository.find_by_id(user_id=user_id, db=db)
        expert.status = UserStatus.ACTIVE

        response : ResponseModel[ExpertResponse] = ResponseModel(
            success=True, 
            data=ExpertResponse(
                username=expert.username,
                email=expert.email,
                role=expert.role,
                id=expert.id
            ),
            message="Expert approved successfully",
        )

        await db.commit()

        return response

    async def reject_expert(self, user_id : int, db : AsyncSession) -> ResponseModel[ExpertResponse] : 

        expert = await self.user_repository.find_by_id(user_id=user_id, db=db)
        expert.status = UserStatus.REJECTED

        response : ResponseModel[ExpertResponse] = ResponseModel(
            success=True, 
            data=ExpertResponse(
                username=expert.username,
                email=expert.email,
                role=expert.role,
                id=expert.id
            ),
            message="Expert rejected"
        )

        await db.commit()

        return response 

    async def dashboard(self, user_id : int, db : AsyncSession) -> ResponseModel[FramerDashboardResponse | AdminDashboardResponse | ExpertDashboardResponse]: 
        user = await self.user_repository.find_by_id(user_id=user_id, db=db)

        if not user : raise NotFound("User not found")

        if user.role == "admin":
            data = await self.user_repository.admin_dashboard(db)
        elif user.role == "expert" : 
            data = await self.user_repository.expert_dashboard(user_id=user_id, db=db)
        else:
            data = await self.user_repository.farmer_dashboard(user.id, db)

        return ResponseModel(
            success=True,
            data=data,
            message="Dashboard retrieved successfully",
            pagination=None
        )
