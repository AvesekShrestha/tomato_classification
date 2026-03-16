from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel

class PostRequest(BaseModel) : 
    title : str
    content : str
    image : Optional[UploadFile] = None
    image_path : Optional[str] = None

