from typing import Optional

from pydantic import BaseModel
from .user_response import UserResponse

class DashboardResponse(BaseModel) : 
    total_posts : int
    total_comments : int
