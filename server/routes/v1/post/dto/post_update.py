from typing import Optional
from pydantic import BaseModel


class PostUpdate(BaseModel) : 
    title : Optional[str] = None
    content : Optional[str] = None
