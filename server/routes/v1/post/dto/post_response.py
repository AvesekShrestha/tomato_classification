from datetime import datetime
from typing import Optional
from pydantic import ConfigDict, BaseModel
from routes.v1.user.dto.user_response import UserResponse

class PostResponse(BaseModel) : 
    
    id : int
    title : str
    content : str
    like : int
    dislike : int
    image : Optional[str] = None
    create_at : datetime
    user : Optional[UserResponse] = None

    model_config = ConfigDict(
            from_attributes=True,
    )
