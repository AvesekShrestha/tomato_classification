from pydantic import BaseModel
from typing import List

class ImageResponse(BaseModel) : 
    predicted_class : str
    cause : str
    prescriptions : List[str]

