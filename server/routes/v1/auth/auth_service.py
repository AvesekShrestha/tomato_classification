from datetime import datetime, timedelta
from routes.v1.auth.dto.login_request import LoginRequest
from routes.v1.auth.dto.login_response import LoginResponse
from routes.v1.auth.dto.register_request import RegisterRequest
from routes.v1.auth.dto.register_response import RegisterResponse
from routes.v1.auth.dto.token_response import TokenResponse
from routes.v1.user.dto.user_response import UserResponse
from routes.v1.user.user_repository import UserRepository
from schemas.refresh_token import RefreshToken
from utils.tokens.token_type import AccessTokenPayload, TokenType
from .auth_repository import AuthRepository
from utils.password.index import check_password, hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from utils.errors.index import TokenExpired, ValueError
from utils.tokens.index import generate_access_token, generate_refresh_token
from routes.v1.token.token_repository import TokenRepository
from routes.v1.token.dto.index import TokenPayload


class AuthService: 

    def __init__(self) : 
        self.auth_repository = AuthRepository()
        self.user_repository = UserRepository()
        self.token_repository = TokenRepository()

    async def refresh(self, ref_token : str, db : AsyncSession) -> TokenResponse: 

        token = await self.token_repository.get_token(ref_token, db)
        
        if token.expires_at < datetime.now() : 
            raise TokenExpired("Refresh token has been expired")

        user_id = token.user_id

        await self.token_repository.delete_token(token, db)

        access_token_payload : AccessTokenPayload = AccessTokenPayload(user_id=user_id, type=TokenType.ACCESS)

        access_token : str = generate_access_token(access_token_payload)
        refresh_token : str = generate_refresh_token()

        payload : RefreshToken = RefreshToken(
            token=refresh_token,
            user_id=user_id,
            expires_at=datetime.now() + timedelta(days=7)
        )

        await self.token_repository.add_token(payload,db)

        tokens : TokenResponse = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
        return tokens

    async def register(self, payload : RegisterRequest, db : AsyncSession) -> RegisterResponse :

        hashed_password = hash_password(payload.password)
        payload = payload.model_copy(update={'password' : hashed_password})
        user = await self.auth_repository.register(payload, db)

        response : RegisterResponse = RegisterResponse(
            username=str(user.username),
            email=user.email,
            role=user.role
        )

        return response


    async def login(self, payload : LoginRequest, db : AsyncSession) -> LoginResponse : 

        user = await self.user_repository.find_by_email(payload.email, db)
        valid_password = check_password(user.password, payload.password)

        if not valid_password : 
            raise ValueError("Invalid passowrd")
        
        user_response : UserResponse = UserResponse(username=user.username, email=user.email, role=user.role)

        access_token_payload : AccessTokenPayload = AccessTokenPayload(user_id=user.id, type=TokenType.ACCESS)

        access_token = generate_access_token(access_token_payload)
        refresh_token = generate_refresh_token()


        refresh_token_payload : TokenPayload = TokenPayload(
            token=refresh_token,
            user_id=user.id,
            expires_at=datetime.now() + timedelta(days=7)
        )
        await self.token_repository.add_token(refresh_token_payload, db)
        tokens : TokenResponse = TokenResponse(access_token=access_token, refresh_token=refresh_token)
        response : LoginResponse = LoginResponse(user=user_response, tokens=tokens)

        return response
