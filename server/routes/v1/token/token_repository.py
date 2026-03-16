from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from schemas.refresh_token import RefreshToken
from sqlalchemy import delete, select
from utils.errors.index import NotFound
from routes.v1.token.dto.index import TokenPayload

class TokenRepository : 

    async def find_by_user_id(self, user_id : int, db : AsyncSession) -> RefreshToken : 

        statement = select(RefreshToken).where(RefreshToken.user_id == user_id)
        result = await db.execute(statement=statement)
        token = result.scalar_one_or_none()

        if not token : 
            raise NotFound("Token not found")

        return token

    async def find_by_token(self, refresh_token : str, db : AsyncSession) -> RefreshToken : 

        statement = select(RefreshToken).options(selectinload(RefreshToken.user)).where(RefreshToken.token == refresh_token)
        result = await db.execute(statement)
        token = result.scalar_one_or_none()

        if not token : 
            raise NotFound("Refresh Token not found")

        return token

    async def add_token(self, payload : TokenPayload, db : AsyncSession) : 
        token = RefreshToken(
            token=payload.token,
            user_id=payload.user_id,
            expires_at=payload.expires_at
        )
        db.add(token)
        await db.flush()

    async def delete_token(self, token : RefreshToken, db : AsyncSession) : 
        await db.delete(token)
        await db.flush()

    async def delete_by_user_id(self, user_id : int, db : AsyncSession):

        statement = delete(RefreshToken).where(RefreshToken.user_id == user_id)
        await db.execute(statement=statement)
        await db.flush()

