from pydantic import BaseModel
from datetime import datetime

class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    likes:int
    dislikes:int
    image:str
    created_at:datetime
    updated_at:datetime

