from pydantic import BaseModel
from enum import Enum

class TokenType(Enum) : 
    ACCESS = "access"
    REFRESH = "refresh"

class AccessTokenPayload(BaseModel) : 
    user_id : int
    type : TokenType = TokenType.ACCESS

class RefreshTokenPayload(BaseModel) : 
    user_id : int
    type : TokenType = TokenType.REFRESH

