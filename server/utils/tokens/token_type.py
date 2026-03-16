from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class TokenType(str, Enum) : 
    ACCESS = "access"
    REFRESH = "refresh"

class AccessTokenPayload(BaseModel) : 
    user_id : int
    type : TokenType = TokenType.ACCESS
    iat : datetime
    exp : datetime
