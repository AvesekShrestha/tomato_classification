from routes.v1.auth.dto.register_request import RegisterRequest
from schemas.user import User
from sqlalchemy.ext.asyncio import AsyncSession

class AuthRepository: 
   
    async def register(self, payload : RegisterRequest, db : AsyncSession) -> User: 
        user = User(
            username=payload.username,
            email=payload.email,
            password=payload.password,
            role=payload.role
        )
        print(user)
        db.add(user)
        await db.flush()
        await db.refresh(user)
        
        return user
       


