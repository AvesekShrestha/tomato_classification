from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional

class PostUpdate(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None
    image:Optional[str]=None
    