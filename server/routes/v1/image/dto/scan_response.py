from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ScanResponse(BaseModel):

    id: int
    image_url: str
    predicted_class: str
    cause: Optional[str]
    prescriptions: Optional[list[str]]
    scanned_at: datetime

    class Config:
        from_attributes = True



