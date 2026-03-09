from sqlalchemy.ext.asyncio import AsyncSession
from schemas.refresh_token import RefreshToken
from sqlalchemy import select
from utils.errors.index import NotFound
from routes.v1.token.dto.index import TokenPayload

class TokenRepository : 

    async def get_token(self, payload : str, db : AsyncSession) -> RefreshToken : 

        statement = select(RefreshToken).where(RefreshToken.token == payload)
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
        await db.commit()

    async def delete_token(self, token : RefreshToken, db : AsyncSession) : 
        await db.delete(token)
        await db.commit()

