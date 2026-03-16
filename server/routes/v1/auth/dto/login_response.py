from typing import Optional
from pydantic import BaseModel
from routes.v1.user.dto.user_response import UserResponse
from routes.v1.auth.dto.token_response import TokenResponse


class LoginResponse(BaseModel) : 
    user : UserResponse
    tokens : Optional[TokenResponse]

