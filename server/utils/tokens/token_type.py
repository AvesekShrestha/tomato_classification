from pydantic import BaseModel
from enum import Enum
from schemas.user import UserRole

class TokenType(str, Enum) : 
    ACCESS = "access"
    REFRESH = "refresh"

class AccessTokenPayload(BaseModel) : 
    user_id : int
    role : UserRole
    type : TokenType = TokenType.ACCESS
    iat : int 
    exp : int  
