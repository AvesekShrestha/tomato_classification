from pydantic import BaseModel

class PostRequest(BaseModel):
    title : str
    content : str
    image : str
    

