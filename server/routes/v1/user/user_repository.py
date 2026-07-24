from datetime import datetime, timedelta
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from routes.v1.user.dto.dashboard_response import DashboardResponse
from schemas.user import User, UserStatus
from utils.errors.index import NotFound
from sqlalchemy import select, func
from typing import List
from schemas.user import UserRole
from schemas.post import Post
from schemas.comment import Comment

class UserRepository: 

    async def find_all(self, db: AsyncSession) -> List[User] :
            statement = select(User)
            result = await db.execute(statement)
            users = result.scalars()._allrows()

            if not users : 
                raise NotFound("Users not found")

            return users 

    async def find_by_id(self, user_id : int, db: AsyncSession) -> User :
        statement = select(User).where(User.id == user_id)
        result = await db.execute(statement)
        user = result.scalar_one_or_none()

        if not user : 
            raise NotFound("User not found")

        return user

    async def find_by_email(self, user_email : EmailStr, db: AsyncSession) -> User | None :
        statement = select(User).where(User.email == user_email)
        result = await db.execute(statement)
        user = result.scalar_one_or_none()

        if not user : 
            # raise NotFound("Email address doesn't match")
            return None

        return user

    async def updateOTP(self, user_id : int, otp : str, db : AsyncSession) :

        user = await self.find_by_id(user_id, db)
        user.otp = otp
        user.otp_expires_at = datetime.now() + timedelta(minutes=5)

        await db.flush()
        await db.refresh(user)

    async def find_experts(self, db : AsyncSession) ->  List[User] : 
        statement = select(User).where(User.role == UserRole.EXPERT, User.status == UserStatus.ACTIVE)
        result = await db.execute(statement)
        experts = result.scalars().all()

        return list(experts)

    async def find_pending_experts(self, db : AsyncSession) ->  List[User] : 
        statement = select(User).where(User.role == UserRole.EXPERT, User.status == UserStatus.PENDING)
        result = await db.execute(statement)
        experts = result.scalars().all()

        return list(experts)

    async def dashboard(self, user_id : int, db : AsyncSession) -> DashboardResponse : 
        
        query = select(
        (
            select(func.count(Post.id))
            .where(Post.user_id == user_id)
            .scalar_subquery()
        ).label("total_posts"),

        (
            select(func.count(Comment.id))
            .where(Comment.user_id == user_id)
            .scalar_subquery()
        ).label("total_comments")
    )

        result = await db.execute(query)
        dashboard = result.one()

        response : DashboardResponse = DashboardResponse(
            total_posts= dashboard.total_posts,
            total_comments = dashboard.total_comments
        )
        
        return response
