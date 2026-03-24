from pydantic import BaseModel

class MessageRequest(BaseModel) : 
    to : int
    message : str
