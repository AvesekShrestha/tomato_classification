from typing import Optional
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from middlewares.auth_middleware import authenticate
from routes.v1.auth.dto.login_request import LoginRequest
from routes.v1.auth.dto.login_response import LoginResponse
from routes.v1.auth.dto.otp import OTPRequest
from routes.v1.auth.dto.register_request import RegisterRequest
from config.database.index import get_db
from routes.v1.auth.dto.register_response import RegisterResponse
from routes.v1.auth.dto.token_response import TokenResponse
from utils.errors.index import InternalServerError
from utils.response.index import ResponseModel 
from .auth_service import AuthService
from sqlalchemy.exc import IntegrityError
from utils.errors.index import ValueError


router = APIRouter()
auth_service = AuthService()


@router.post("/verify-otp", response_model=ResponseModel[None], response_model_exclude_none=True)
async def verifyOTP(payload : OTPRequest, db : AsyncSession = Depends(get_db), user_id : int = Depends(authenticate)) -> ResponseModel[None] :
    
    await auth_service.verify_OTP(user_id=user_id, payload=payload, db=db)

    return ResponseModel[None](
        success=True,
        data=None,
        message="OTP verified successfully"
    )

@router.post("/refresh", response_model_exclude_none=True, response_model=ResponseModel[TokenResponse])
async def refresh(request : Request, response : Response, refresh_token : Optional[str] = None, db : AsyncSession = Depends(get_db)) -> ResponseModel[TokenResponse]: 

    token = None
    if not refresh_token : 
        token = request.cookies.get("refreshToken")

    if not token:
        raise ValueError("Missing Refresh Token")

    res : TokenResponse = await auth_service.refresh(token, db)
    if not res.refresh_token : 
        raise ValueError("Refresh Token is not generated")

    response.set_cookie("refreshToken", res.refresh_token, samesite="lax", httponly=True)

    tokens : TokenResponse = res.model_copy(update={"refresh_token" : None})
    
    return ResponseModel[TokenResponse](
        success=True,
        data=tokens,
        message="Refreshed successfully"
    )


@router.post("/register", response_model_exclude_none=True, response_model=ResponseModel[RegisterResponse])
async def register(payload : RegisterRequest, db : AsyncSession = Depends(get_db)) -> ResponseModel[RegisterResponse]: 
    try : 
        response = await auth_service.register(payload, db)
        return ResponseModel[RegisterResponse](success=True, data=response, message="User registered successfull")
        
    except IntegrityError as e:
        detail_message = getattr(e.orig, 'detail', str(e.orig))
        raise ValueError(detail_message)
        
    except Exception as e:
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.post("/login", response_model_exclude_none=True)
async def login(res : Response, payload : LoginRequest, db:AsyncSession = Depends(get_db)) -> ResponseModel[LoginResponse] : 
    try:
        MAX_AGE = 15 * 24 * 60 * 60

        response = await auth_service.login(payload, db)

        if response.tokens.refresh_token is None : 
            raise InternalServerError("Refresh token is not generated")
        
        res.set_cookie(
            key="refreshToken",
            value=response.tokens.refresh_token,
            samesite="lax",
            httponly=True,
            max_age=MAX_AGE
        )

        tokens = response.tokens.model_copy(update={"refresh_token" : None})
        response = response.model_copy(update={"tokens" : tokens})

        return ResponseModel[LoginResponse](success=True, data=response, message="User looged in successfully")

    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)
