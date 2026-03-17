from pydantic import BaseModel


class CommentRequest(BaseModel) : 
    content : str
