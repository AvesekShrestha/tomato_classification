from pydantic import BaseModel
from schemas.reaction import TargetType

class ReactionRequest(BaseModel) : 

    is_like : bool
    target_id : int
    target_type : TargetType 
