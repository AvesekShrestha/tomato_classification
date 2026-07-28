from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ScanRequest(BaseModel):

    image_url: str
    predicted_class: str
    cause: Optional[str] = None
    prescriptions: Optional[list[str]] = None

