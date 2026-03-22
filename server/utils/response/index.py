from pydantic import BaseModel
from typing import Generic, Optional, TypeVar


T = TypeVar("T")

class Pagination(BaseModel) : 
    next_cursor : Optional[str] = None
    has_more : bool

class ResponseModel(BaseModel, Generic[T]) : 
    success : bool
    data : Optional[T] = None 
    message : Optional[str] = None
    pagination : Optional[Pagination] = None
