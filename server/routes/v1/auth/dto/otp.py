from typing import Optional
from pydantic import BaseModel, EmailStr

class OTPRequest(BaseModel) : 
    email : EmailStr
    otp : Optional[str] = None

class OTPResponse(BaseModel) : 
    otp : str
