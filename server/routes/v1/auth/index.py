from fastapi import APIRouter
from routes.v1.auth.dto.login_request import LoginRequest
from routes.v1.auth.dto.register_request import RegisterRequest


router = APIRouter()

@router.post("/register")
async def register(payload : RegisterRequest) : 
    pass


@router.post("/login")
async def login(payload : LoginRequest) : 
    pass 
