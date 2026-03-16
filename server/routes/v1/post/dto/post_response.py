from typing import Optional
from pydantic import ConfigDict, BaseModel

class PostResponse(BaseModel) : 
    
    id : int
    title : str
    content : str
    like : int
    dislike : int
    image : Optional[str] = None

    model_config = ConfigDict(
            from_attributes=True,
    )
