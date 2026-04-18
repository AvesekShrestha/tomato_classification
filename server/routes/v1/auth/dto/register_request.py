from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator 
from routes.v1.user.dto.user_role import UserRole
from schemas.user import UserStatus
from utils.errors.index import ValueError

class RegisterRequest(BaseModel) : 
    username : str
    email : EmailStr
    password : str
    role : Optional[UserRole] = UserRole.FARMER
    status : Optional[UserStatus] = UserStatus.ACTIVE

    @field_validator("password")
    @classmethod
    def password_strength(cls, value) :

        if len(value) < 8 : 
            raise ValueError("Password length should be greater than 8")

        return value
