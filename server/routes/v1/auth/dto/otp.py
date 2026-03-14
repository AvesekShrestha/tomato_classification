from typing import Optional
from pydantic import BaseModel, EmailStr

class OTPRequest(BaseModel) : 
    email : EmailStr
    otp : str

class OTPResponse(BaseModel) : 
    otp : str
