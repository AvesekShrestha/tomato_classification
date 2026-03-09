from datetime import datetime 
from pydantic import BaseModel 


class TokenPayload(BaseModel) : 

    token : str
    user_id : int
    expires_at : datetime
