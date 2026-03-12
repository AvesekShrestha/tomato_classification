from datetime import datetime, timedelta
from fastapi import Depends
from config.database.index import get_db
from routes.v1.auth.dto.login_request import LoginRequest
from routes.v1.auth.dto.login_response import LoginResponse
from routes.v1.auth.dto.register_request import RegisterRequest
from routes.v1.auth.dto.register_response import RegisterResponse
from routes.v1.auth.dto.token_response import TokenResponse
from routes.v1.token import token_repository
from routes.v1.user.dto.user_response import UserResponse
from routes.v1.user.user_repository import UserRepository
from schemas.refresh_token import RefreshToken
from utils.tokens.token_type import AccessTokenPayload, TokenType
from .auth_repository import AuthRepository
from utils.password.index import check_password, hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from utils.errors.index import BadRequest, InternalServerError, TokenExpired, ValueError, OTPExpired
from utils.tokens.index import generate_access_token, generate_refresh_token
from routes.v1.token.token_repository import TokenRepository
from routes.v1.token.dto.index import TokenPayload
from utils.otp.index import generate_otp
from utils.mail.index import send_mail
from routes.v1.auth.dto.otp import OTPRequest

class AuthService: 

    def __init__(self) : 
        self.auth_repository = AuthRepository()
        self.user_repository = UserRepository()
        self.token_repository = TokenRepository()

    async def resend_OTP(self, payload : OTPRequest, db : AsyncSession = Depends(get_db)) : 

        if not payload.email : 
            raise ValueError("Email address is required for resending otp")

        user = await self.user_repository.find_by_email(user_email=payload.email, db=db)
        otp = generate_otp()
        send_mail(otp=otp, to=payload.email)
        user.otp = otp

        await db.commit()

    async def verify_OTP(self, user_id : int, payload : OTPRequest, db : AsyncSession)-> None :
        user = await self.user_repository.find_by_id(user_id=user_id, db=db)

        if not payload.otp :
            raise ValueError("OTP required for verfiying")

        if not user.otp :
            raise InternalServerError("OTP is not present")

        if not user.otp_expires_at :
            raise InternalServerError("OTP expired")

        if user.otp_expires_at < datetime.now() : 
            raise OTPExpired("OTP has been expired")

        if user.otp != payload.otp : 
            raise BadRequest("Invalid OTP")

        user.is_verified = True
        user.otp = None
        user.otp_expires_at = None

        await db.commit()

        return None

    async def refresh(self, ref_token : str, db : AsyncSession) -> TokenResponse: 

        token = await self.token_repository.find_by_token(ref_token, db)
        
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

        otp : str = generate_otp()

        await self.user_repository.updateOTP(user_id=user.id, otp=otp, db=db)
        send_mail(otp, user.email)

        response : RegisterResponse = RegisterResponse(
            username=str(user.username),
            email=user.email,
            role=user.role
        )
        await db.commit()

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

    async def logout(self, user_id : int, db : AsyncSession) -> None :

        await self.token_repository.delete_by_user_id(user_id=user_id, db=db)
        return None
        

        
