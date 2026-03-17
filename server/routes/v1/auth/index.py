from fastapi import APIRouter, BackgroundTasks, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from middlewares.auth_middleware import current_user_id
from routes.v1.auth.dto.login_request import LoginRequest
from routes.v1.auth.dto.login_response import LoginResponse
from routes.v1.auth.dto.otp import OTPRequest, OTPResponse
from routes.v1.auth.dto.register_request import RegisterRequest
from config.database.index import get_db
from routes.v1.auth.dto.register_response import RegisterResponse
from routes.v1.auth.dto.token_response import TokenResponse
from utils.errors.index import InternalServerError, Unauthorized
from utils.response.index import ResponseModel 
from .auth_service import AuthService
from sqlalchemy.exc import IntegrityError
from utils.errors.index import ValueError


router = APIRouter()
auth_service = AuthService()

@router.post("/resend-otp", response_model=ResponseModel[OTPResponse], response_model_exclude_none=True)
async def resend_otp(payload : OTPRequest, background_task : BackgroundTasks, db : AsyncSession = Depends(get_db)) -> ResponseModel[OTPResponse] :

    try:
        response = await auth_service.resend_OTP(payload, background_task, db)
        return ResponseModel[OTPResponse](
            success=True,
            data=response,
            message="OTP has been resent successfully"
        )
    except Exception as e : 
        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.post("/verify-otp", response_model=ResponseModel[None], response_model_exclude_none=True)
async def verifyOTP(payload : OTPRequest, db : AsyncSession = Depends(get_db)) -> ResponseModel[None] :
    
    await auth_service.verify_OTP(payload=payload, db=db)

    return ResponseModel[None](
        success=True,
        data=None,
        message="OTP verified successfully"
    )

@router.post("/refresh", response_model_exclude_none=True, response_model=ResponseModel[TokenResponse])
async def refresh(request : Request, response : Response, db : AsyncSession = Depends(get_db)) -> ResponseModel[TokenResponse]: 

    token = request.cookies.get("refreshToken")
    if not token:
        raise Unauthorized("Session Expired")

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
async def register(payload : RegisterRequest, background_task : BackgroundTasks, db : AsyncSession = Depends(get_db)) -> ResponseModel[RegisterResponse]: 
    try : 
        print("Hello from register controller")
        response = await auth_service.register(payload, background_task, db)
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
        REFRESH_TOKEN_MAX_AGE = 15 * 24 * 60 * 60
        ACCESS_TOKEN_MAX_AGE = 5 * 60 * 60

        response = await auth_service.login(payload=payload, db=db)

        if not response.tokens :
            raise InternalServerError("No tokens generated")

        if response.tokens.refresh_token is None : 
            raise InternalServerError("Refresh token is not generated")
        
        res.set_cookie(
            key="refreshToken",
            value=response.tokens.refresh_token,
            samesite="lax",
            httponly=True,
            max_age=REFRESH_TOKEN_MAX_AGE
        )
        
        res.set_cookie(
            key="accessToken",
            value=response.tokens.access_token,
            samesite="lax",
            httponly=True,
            max_age=ACCESS_TOKEN_MAX_AGE
        )

        response = response.model_copy(update={"tokens" : None})
        return ResponseModel[LoginResponse](success=True, data=response, message="User looged in successfully")

    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)

@router.post("/logout", response_model_exclude_none=True, response_model=ResponseModel[None])
async def logout(response : Response, db : AsyncSession = Depends(get_db), user_id : int = Depends(current_user_id)) -> ResponseModel[None] :
    try:
        response.delete_cookie(
            key="refreshToken",
            httponly=True,
            samesite="lax"
        )
        response.delete_cookie(
            key="accessToken",
            httponly=True,
            samesite="lax"
        )

        await auth_service.logout(user_id=user_id, db=db)

        return ResponseModel[None](
            success=True,
            data=None,
            message="Logout successfully"
        )
        
    except Exception as e : 
        error_message = e.args[0] if e.args[0] else str(e)
        raise  InternalServerError(error_message)
