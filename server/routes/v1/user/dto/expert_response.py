from typing import Optional
from .user_response import UserResponse

class ExpertResponse(UserResponse) : 
    id : int
    online :  Optional[bool] = None
