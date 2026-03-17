from typing import Optional
from pydantic import BaseModel


class PostUpdate(BaseModel) : 
    title : Optional[str]
    content : Optional[str]

