from datetime import datetime
from pydantic import BaseModel

class ChatResponse(BaseModel) : 
    message : str
    sender_id : int
    receiver_id : int
    is_read : bool
    messaged_at : datetime
