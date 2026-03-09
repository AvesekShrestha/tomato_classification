from pydantic import BaseModel, EmailStr, ConfigDict

from routes.v1.user.dto.user_role import UserRole

class UserResponse(BaseModel) : 

    username : str
    email : EmailStr
    role : UserRole

    model_config = ConfigDict(
        from_attributes=True,
    )

