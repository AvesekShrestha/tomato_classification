from typing import Optional
from .user_response import UserResponse

class ExpertResponse(UserResponse) : 
    online :  Optional[bool] = None
