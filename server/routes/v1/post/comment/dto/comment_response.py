from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from routes.v1.user.dto.user_response import UserResponse


class CommentResponse(BaseModel) : 
    id : int
    content : str
    like : int
    dislike : int 
    created_at : datetime
    user : Optional[UserResponse] = None
