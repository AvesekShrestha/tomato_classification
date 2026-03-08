from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import User
from utils.errors.index import NotFound
from sqlalchemy import select

class UserRepository: 

    async def find_by_id(self, user_id : int, db: AsyncSession) -> User :
        statement = select(User).where(User.id == user_id)
        result = await db.execute(statement)
        user = result.scalar_one_or_none()

        if not user : 
            raise NotFound("User not found")

        return user

    async def find_by_email(self, user_email : int, db: AsyncSession) -> User :
        statement = select(User).where(User.email == user_email)
        result = await db.execute(statement)
        user = result.scalar_one_or_none()

        if not user : 
            raise NotFound("User not found")

        return user
