from routes.v1.user.dto.user_response import UserResponse
from .user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

class UserService: 

    def __init__(self) : 
        self.user_repository = UserRepository()

    async def find_all(self, db: AsyncSession) -> List[UserResponse]: 
        users = await self.user_repository.find_all(db)
        response : List[UserResponse] = [
            UserResponse(
                username=user.username,
                email=user.email,
                role=user.role
            )
            for user in users
        ]
        return response

    async def find_by_id(self, user_id, db: AsyncSession) -> UserResponse: 
       
        user = await self.user_repository.find_by_id(user_id, db)
        response : UserResponse = UserResponse(
            username=user.username,
            email=user.email,
            role=user.role
        )
        return response
        
    async def find_by_email(self, user_email, db: AsyncSession) -> UserResponse :
        user = await self.user_repository.find_by_id(user_email, db)
        response : UserResponse = UserResponse(
            username=user.username,
            email=user.email,
            role=user.role
        )

        return response

    async def me(self, user_id : int, db : AsyncSession) -> UserResponse : 

        user = await self.user_repository.find_by_id(user_id=user_id, db=db)
        return user
