from routes.v1.auth.dto.register_request import RegisterRequest
from schemas.user import User
from sqlalchemy.ext.asyncio import AsyncSession

class AuthRepository: 

    async def register(self, payload : RegisterRequest, db : AsyncSession) -> User: 
        user = User(payload)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return user
       


