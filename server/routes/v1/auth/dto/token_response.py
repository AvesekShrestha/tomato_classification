from typing import Optional
from pydantic import BaseModel, ConfigDict, model_serializer

class TokenResponse(BaseModel) : 

    access_token : str
    refresh_token : Optional[str] = None
   
    model_config = ConfigDict(
        from_attributes=True,
    )

    @model_serializer
    def serialize(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}
