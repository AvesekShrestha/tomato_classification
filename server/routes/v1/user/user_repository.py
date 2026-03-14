from datetime import datetime, timedelta
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import User
from utils.errors.index import NotFound
from sqlalchemy import select
from typing import List

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

    async def find_by_email(self, user_email : EmailStr, db: AsyncSession) -> User :
        statement = select(User).where(User.email == user_email)
        result = await db.execute(statement)
        user = result.scalar_one_or_none()

        if not user : 
            raise NotFound("User not found")

        return user

    async def updateOTP(self, user_id : int, otp : str, db : AsyncSession) :

        user = await self.find_by_id(user_id, db)
        user.otp = otp
        user.otp_expires_at = datetime.now() + timedelta(minutes=5)

        await db.flush()
        await db.refresh(user)

