from routes.v1.auth.dto.login_request import LoginRequest
from routes.v1.auth.dto.login_response import LoginResponse
from routes.v1.auth.dto.register_request import RegisterRequest
from routes.v1.auth.dto.register_response import RegisterResponse
from .auth_repository import AuthRepository
from utils.password.index import hash_password
from sqlalchemy.ext.asyncio import AsyncSession

class AuthService: 

    def __init__(self) : 
        self.auth_repository = AuthRepository()

    async def register(self, payload : RegisterRequest, db : AsyncSession) -> RegisterResponse :

        hashed_password = hash_password(payload.password)
        payload = payload.model_copy(update={'password' : hashed_password})
        user = await self.auth_repository.register(payload, db)

        response : RegisterResponse = RegisterResponse(
            username=user.username,
            email=user.email
        )

        return response


    async def login(self, payload : LoginRequest, db : AsyncSession) -> LoginResponse : 
        pass



