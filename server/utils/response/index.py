from pydantic import BaseModel
from typing import Generic, Optional, TypeVar


T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]) : 
    success : bool
    data : Optional[T] = None 
    message : Optional[str] = None

