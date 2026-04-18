from pydantic import BaseModel
from typing import List, Optional

class ImageResponse(BaseModel) : 
    predicted_class : str
    cause : Optional[str] = None
    prescriptions : Optional[List[str]] = None

