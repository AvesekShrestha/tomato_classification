from pydantic import ConfigDict, BaseModel

class PostResponse(BaseModel) : 
    
    id : int
    title : str
    content : str
    like : int
    dislike : int

    model_config = ConfigDict(
            from_attributes=True,
    )
