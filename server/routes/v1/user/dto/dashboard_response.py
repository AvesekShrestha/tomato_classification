from typing import Optional

from pydantic import BaseModel
from .user_response import UserResponse

class FramerDashboardResponse(BaseModel) : 
    total_posts : int
    total_comments : int
    total_scans: int

class AdminDashboardResponse(BaseModel):
    total_farmers: int
    total_experts: int
    total_users: int
    total_posts: int
    total_comments : int

class ExpertDashboardResponse(BaseModel) : 
    total_farmers : int
    total_posts : int
    total_comments : int
    total_scans: int
